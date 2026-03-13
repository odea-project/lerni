from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Block:
    block_id: str
    kind: str
    text: str | None = None
    items: list[str] = field(default_factory=list)
    code: str | None = None
    language: str | None = None
    reveal_step: int | None = None


@dataclass(slots=True)
class Region:
    name: str
    blocks: list[Block] = field(default_factory=list)


@dataclass(slots=True)
class RevealGroup:
    step: int
    block_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InteractionReference:
    kind: str
    region_names: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Slide:
    slide_id: str
    kind: str | None = None
    template: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    regions: list[Region] = field(default_factory=list)
    reveal_groups: list[RevealGroup] = field(default_factory=list)
    interactions: list[InteractionReference] = field(default_factory=list)


@dataclass(slots=True)
class Deck:
    deck_id: str
    metadata: dict[str, str] = field(default_factory=dict)
    slides: list[Slide] = field(default_factory=list)