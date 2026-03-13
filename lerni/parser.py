from __future__ import annotations

from dataclasses import dataclass
import re

from .document_model import Block, Deck, InteractionReference, Region, RevealGroup, Slide


SLIDE_SPLIT_RE = re.compile(r"^---\s*$", re.MULTILINE)
SLIDE_DIRECTIVE_RE = re.compile(r"^::slide\s*(.*)$")
REGION_DIRECTIVE_RE = re.compile(r"^::region\s+([a-z_][a-z0-9_]*)\s*$")
REVEAL_DIRECTIVE_RE = re.compile(r"^::reveal\s+step=(\d+)\s*$")


class ParseError(ValueError):
    pass


@dataclass(slots=True)
class _SlideMetadata:
    kind: str | None
    template: str | None
    metadata: dict[str, str]


def parse_document(source: str, deck_id: str = "deck-1") -> Deck:
    normalized = source.replace("\r\n", "\n").strip()
    if not normalized:
        raise ParseError("Source is empty.")

    raw_slides = [chunk.strip() for chunk in SLIDE_SPLIT_RE.split(normalized) if chunk.strip()]
    if not raw_slides:
        raise ParseError("No slides found in source.")

    deck = Deck(deck_id=deck_id)
    for index, raw_slide in enumerate(raw_slides, start=1):
        deck.slides.append(_parse_slide(raw_slide, index))
    return deck


def _parse_slide(raw_slide: str, slide_index: int) -> Slide:
    lines = raw_slide.split("\n")
    cursor = 0
    metadata = _SlideMetadata(kind=None, template=None, metadata={})

    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1

    if cursor < len(lines):
        match = SLIDE_DIRECTIVE_RE.match(lines[cursor].strip())
        if match:
            metadata = _parse_slide_metadata(match.group(1), slide_index)
            cursor += 1

    title_region: Region | None = None
    if cursor < len(lines) and lines[cursor].startswith("# "):
        title_text = lines[cursor][2:].strip()
        title_region = Region(
            name="title",
            blocks=[Block(block_id=f"slide-{slide_index}-title-1", kind="heading", text=title_text)],
        )
        cursor += 1

    remaining = lines[cursor:]
    regions, reveal_groups = _parse_regions(remaining, slide_index)
    if title_region is not None:
        regions.insert(0, title_region)

    if not regions:
        raise ParseError(f"Slide {slide_index} has no supported semantic regions.")

    return Slide(
        slide_id=f"slide-{slide_index}",
        kind=metadata.kind,
        template=metadata.template,
        metadata=metadata.metadata,
        regions=regions,
        reveal_groups=reveal_groups,
        interactions=_infer_interactions(regions),
    )


def _parse_slide_metadata(metadata_fragment: str, slide_index: int) -> _SlideMetadata:
    metadata: dict[str, str] = {}
    kind: str | None = None
    template: str | None = None
    if not metadata_fragment.strip():
        return _SlideMetadata(kind=None, template=None, metadata={})

    for token in metadata_fragment.split():
        if "=" not in token:
            raise ParseError(f"Slide {slide_index} contains invalid slide metadata token: {token}")
        key, value = token.split("=", 1)
        if key == "kind":
            kind = value
        elif key == "template":
            template = value
        else:
            metadata[key] = value
    return _SlideMetadata(kind=kind, template=template, metadata=metadata)


def _parse_regions(lines: list[str], slide_index: int) -> tuple[list[Region], list[RevealGroup]]:
    regions: list[Region] = []
    reveal_groups: list[RevealGroup] = []
    current_region_name: str | None = None
    current_region_lines: list[str] = []
    seen_region_names: set[str] = set()

    def flush_region() -> None:
        nonlocal current_region_name, current_region_lines
        if current_region_name is None:
            return
        blocks, region_reveals = _parse_region_blocks(current_region_lines, slide_index, current_region_name)
        regions.append(Region(name=current_region_name, blocks=blocks))
        reveal_groups.extend(region_reveals)
        current_region_name = None
        current_region_lines = []

    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped and current_region_name is None:
            continue

        region_match = REGION_DIRECTIVE_RE.match(stripped)
        if region_match:
            flush_region()
            current_region_name = region_match.group(1)
            if current_region_name in seen_region_names:
                raise ParseError(f"Slide {slide_index} repeats region '{current_region_name}'.")
            seen_region_names.add(current_region_name)
            continue

        if stripped.startswith("::") and current_region_name is None:
            raise ParseError(f"Slide {slide_index} contains unsupported directive before any region on line {line_number}.")

        if current_region_name is None:
            raise ParseError(
                f"Slide {slide_index} contains content outside supported regions on line {line_number}: {raw_line!r}"
            )
        current_region_lines.append(raw_line)

    flush_region()
    return regions, reveal_groups


def _parse_region_blocks(lines: list[str], slide_index: int, region_name: str) -> tuple[list[Block], list[RevealGroup]]:
    blocks: list[Block] = []
    reveal_groups: list[RevealGroup] = []
    cursor = 0
    block_counter = 0

    def next_block_id() -> str:
        nonlocal block_counter
        block_counter += 1
        return f"slide-{slide_index}-{region_name}-{block_counter}"

    while cursor < len(lines):
        stripped = lines[cursor].strip()
        if not stripped:
            cursor += 1
            continue

        reveal_match = REVEAL_DIRECTIVE_RE.match(stripped)
        if reveal_match:
            step = int(reveal_match.group(1))
            reveal_content: list[str] = []
            cursor += 1
            while cursor < len(lines) and lines[cursor].strip() != "::endreveal":
                reveal_content.append(lines[cursor])
                cursor += 1
            if cursor >= len(lines):
                raise ParseError(f"Slide {slide_index} region '{region_name}' has an unclosed reveal block.")
            nested_blocks, _ = _parse_region_blocks(reveal_content, slide_index, region_name)
            block_ids: list[str] = []
            for block in nested_blocks:
                block.reveal_step = step
                if block.block_id.endswith("-1") and any(existing.block_id == block.block_id for existing in blocks):
                    block.block_id = next_block_id()
                block_ids.append(block.block_id)
                blocks.append(block)
            reveal_groups.append(RevealGroup(step=step, block_ids=block_ids))
            cursor += 1
            continue

        if stripped == "::endreveal":
            raise ParseError(f"Slide {slide_index} region '{region_name}' contains an unmatched ::endreveal.")

        if stripped.startswith("::"):
            raise ParseError(
                f"Slide {slide_index} region '{region_name}' contains unsupported directive: {stripped}"
            )

        if stripped.startswith("```"):
            language = stripped[3:].strip() or None
            cursor += 1
            code_lines: list[str] = []
            while cursor < len(lines) and not lines[cursor].strip().startswith("```"):
                code_lines.append(lines[cursor])
                cursor += 1
            if cursor >= len(lines):
                raise ParseError(f"Slide {slide_index} region '{region_name}' contains an unclosed code fence.")
            blocks.append(Block(block_id=next_block_id(), kind="code", code="\n".join(code_lines), language=language))
            cursor += 1
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while cursor < len(lines) and lines[cursor].strip().startswith("- "):
                items.append(lines[cursor].strip()[2:].strip())
                cursor += 1
            blocks.append(Block(block_id=next_block_id(), kind="list", items=items))
            continue

        paragraph_lines: list[str] = []
        while cursor < len(lines):
            current = lines[cursor].strip()
            if not current:
                break
            if current.startswith("::") or current.startswith("```") or current.startswith("- "):
                break
            paragraph_lines.append(lines[cursor].strip())
            cursor += 1
        blocks.append(Block(block_id=next_block_id(), kind="paragraph", text=" ".join(paragraph_lines)))

    return blocks, reveal_groups


def _infer_interactions(regions: list[Region]) -> list[InteractionReference]:
    region_names = {region.name for region in regions}
    interactions: list[InteractionReference] = []

    if "question" in region_names or "answer_choices" in region_names:
        relevant = [name for name in ["question", "answer_choices", "feedback"] if name in region_names]
        interactions.append(InteractionReference(kind="question_flow", region_names=relevant))

    if any(block.reveal_step is not None for region in regions for block in region.blocks):
        interactions.append(
            InteractionReference(
                kind="guided_reveal",
                region_names=[region.name for region in regions if any(block.reveal_step is not None for block in region.blocks)],
            )
        )

    return interactions