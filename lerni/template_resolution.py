from __future__ import annotations

from dataclasses import dataclass, field

from .document_model import Block, Deck, InteractionReference, Region, RevealGroup, Slide


CONTENT_BLOCK_KINDS = frozenset({"paragraph", "list", "code"})


@dataclass(frozen=True, slots=True)
class SlotContract:
    name: str
    required: bool
    allowed_block_kinds: frozenset[str]


@dataclass(frozen=True, slots=True)
class TemplateContract:
    template_id: str
    supported_slide_kinds: frozenset[str]
    slots: tuple[SlotContract, ...]


@dataclass(frozen=True, slots=True)
class ResolutionIssue:
    code: str
    message: str
    slot_name: str | None = None
    region_name: str | None = None


@dataclass(slots=True)
class ResolvedSlot:
    slot_name: str
    region_name: str
    blocks: list[Block]


@dataclass(slots=True)
class ResolvedTemplateSlide:
    slide_id: str
    template_id: str
    slide_kind: str | None
    slot_bindings: dict[str, ResolvedSlot]
    omitted_optional_slots: list[str] = field(default_factory=list)
    reveal_groups: list[RevealGroup] = field(default_factory=list)
    interactions: list[InteractionReference] = field(default_factory=list)


class TemplateResolutionError(ValueError):
    def __init__(self, slide_id: str, issues: list[ResolutionIssue]):
        self.slide_id = slide_id
        self.issues = issues
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        issue_summary = "; ".join(issue.message for issue in self.issues)
        return f"Slide '{self.slide_id}' failed template resolution: {issue_summary}"


TITLE_OVERVIEW_CONTRACT = TemplateContract(
    template_id="title-overview",
    supported_slide_kinds=frozenset({"overview"}),
    slots=(
        SlotContract(name="title", required=True, allowed_block_kinds=frozenset({"heading"})),
        SlotContract(name="explanation", required=True, allowed_block_kinds=CONTENT_BLOCK_KINDS),
        SlotContract(name="example", required=False, allowed_block_kinds=CONTENT_BLOCK_KINDS),
    ),
)


QUIZ_FEEDBACK_CONTRACT = TemplateContract(
    template_id="quiz-feedback",
    supported_slide_kinds=frozenset({"quiz"}),
    slots=(
        SlotContract(name="title", required=True, allowed_block_kinds=frozenset({"heading"})),
        SlotContract(name="question", required=True, allowed_block_kinds=CONTENT_BLOCK_KINDS),
        SlotContract(name="answer_choices", required=True, allowed_block_kinds=frozenset({"list"})),
        SlotContract(name="feedback", required=True, allowed_block_kinds=CONTENT_BLOCK_KINDS),
    ),
)


TEMPLATE_CONTRACTS: dict[str, TemplateContract] = {
    TITLE_OVERVIEW_CONTRACT.template_id: TITLE_OVERVIEW_CONTRACT,
    QUIZ_FEEDBACK_CONTRACT.template_id: QUIZ_FEEDBACK_CONTRACT,
}

DEFAULT_TEMPLATES_BY_KIND = {
    "overview": "title-overview",
    "quiz": "quiz-feedback",
}


def resolve_deck_templates(deck: Deck) -> list[ResolvedTemplateSlide]:
    return [resolve_slide_template(slide) for slide in deck.slides]


def resolve_slide_template(slide: Slide) -> ResolvedTemplateSlide:
    contract = _select_template_contract(slide)
    issues: list[ResolutionIssue] = []
    slot_bindings: dict[str, ResolvedSlot] = {}
    region_map = {region.name: region for region in slide.regions}
    expected_slot_names = {slot.name for slot in contract.slots}
    omitted_optional_slots: list[str] = []

    for slot in contract.slots:
        region = region_map.get(slot.name)
        if region is None:
            if slot.required:
                issues.append(
                    ResolutionIssue(
                        code="missing_required_slot",
                        message=f"Template '{contract.template_id}' requires region '{slot.name}'.",
                        slot_name=slot.name,
                    )
                )
            else:
                omitted_optional_slots.append(slot.name)
            continue

        if not region.blocks:
            issues.append(
                ResolutionIssue(
                    code="empty_slot_region",
                    message=(
                        f"Region '{region.name}' does not contain any blocks for slot '{slot.name}' in "
                        f"template '{contract.template_id}'."
                    ),
                    slot_name=slot.name,
                    region_name=region.name,
                )
            )
            continue

        incompatible_blocks = [block.kind for block in region.blocks if block.kind not in slot.allowed_block_kinds]
        if incompatible_blocks:
            issues.append(
                ResolutionIssue(
                    code="incompatible_block_kind",
                    message=(
                        f"Region '{region.name}' is incompatible with slot '{slot.name}' in template "
                        f"'{contract.template_id}': {', '.join(incompatible_blocks)}"
                    ),
                    slot_name=slot.name,
                    region_name=region.name,
                )
            )
            continue

        slot_bindings[slot.name] = ResolvedSlot(
            slot_name=slot.name,
            region_name=region.name,
            blocks=list(region.blocks),
        )

    for region in slide.regions:
        if region.name not in expected_slot_names:
            issues.append(
                ResolutionIssue(
                    code="unsupported_region",
                    message=f"Template '{contract.template_id}' does not declare region '{region.name}'.",
                    region_name=region.name,
                )
            )

    if issues:
        raise TemplateResolutionError(slide.slide_id, issues)

    return ResolvedTemplateSlide(
        slide_id=slide.slide_id,
        template_id=contract.template_id,
        slide_kind=slide.kind,
        slot_bindings=slot_bindings,
        omitted_optional_slots=omitted_optional_slots,
        reveal_groups=list(slide.reveal_groups),
        interactions=list(slide.interactions),
    )


def _select_template_contract(slide: Slide) -> TemplateContract:
    template_id = slide.template
    if template_id is None:
        if slide.kind is None:
            raise TemplateResolutionError(
                slide.slide_id,
                [
                    ResolutionIssue(
                        code="template_selection_failed",
                        message="Slide does not declare a template and has no slide kind for default resolution.",
                    )
                ],
            )
        template_id = DEFAULT_TEMPLATES_BY_KIND.get(slide.kind)
        if template_id is None:
            raise TemplateResolutionError(
                slide.slide_id,
                [
                    ResolutionIssue(
                        code="template_selection_failed",
                        message=f"No default template is registered for slide kind '{slide.kind}'.",
                    )
                ],
            )

    contract = TEMPLATE_CONTRACTS.get(template_id)
    if contract is None:
        raise TemplateResolutionError(
            slide.slide_id,
            [
                ResolutionIssue(
                    code="unknown_template",
                    message=f"Template '{template_id}' is not supported by the MVP resolver.",
                )
            ],
        )

    if slide.kind is not None and slide.kind not in contract.supported_slide_kinds:
        raise TemplateResolutionError(
            slide.slide_id,
            [
                ResolutionIssue(
                    code="template_kind_mismatch",
                    message=(
                        f"Template '{contract.template_id}' does not support slide kind '{slide.kind}'."
                    ),
                )
            ],
        )

    return contract