from __future__ import annotations

from dataclasses import dataclass

from .document_model import Block
from .template_resolution import ResolvedSlot, ResolvedTemplateSlide


SUPPORTED_INTERACTIONS = frozenset({"guided_reveal", "question_flow"})


@dataclass(frozen=True, slots=True)
class RuntimeSlotVisibility:
    slot_name: str
    visible_block_ids: list[str]
    hidden_block_ids: list[str]


@dataclass(frozen=True, slots=True)
class SlideRuntimeSnapshot:
    slide_id: str
    template_id: str
    current_reveal_step: int
    max_reveal_step: int
    can_advance_reveal: bool
    selected_answer_index: int | None
    feedback_visible: bool
    active_mode: str
    slot_visibility: dict[str, RuntimeSlotVisibility]


class InteractionRuntimeError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class SlideInteractionRuntime:
    def __init__(self, resolved_slide: ResolvedTemplateSlide):
        self._resolved_slide = resolved_slide
        self._current_reveal_step = 0
        self._selected_answer_index: int | None = None
        self._feedback_visible = False
        self._max_reveal_step = max(
            (block.reveal_step or 0)
            for slot in resolved_slide.slot_bindings.values()
            for block in slot.blocks
        )
        self._answer_count = self._derive_answer_count()
        self._validate_runtime_shape()

    @property
    def resolved_slide(self) -> ResolvedTemplateSlide:
        return self._resolved_slide

    def snapshot(self) -> SlideRuntimeSnapshot:
        slot_visibility = {
            slot_name: self._build_slot_visibility(slot_name, resolved_slot)
            for slot_name, resolved_slot in self._resolved_slide.slot_bindings.items()
        }
        return SlideRuntimeSnapshot(
            slide_id=self._resolved_slide.slide_id,
            template_id=self._resolved_slide.template_id,
            current_reveal_step=self._current_reveal_step,
            max_reveal_step=self._max_reveal_step,
            can_advance_reveal=self._current_reveal_step < self._max_reveal_step,
            selected_answer_index=self._selected_answer_index,
            feedback_visible=self._feedback_visible,
            active_mode=self._derive_active_mode(),
            slot_visibility=slot_visibility,
        )

    def advance_reveal(self) -> SlideRuntimeSnapshot:
        if self._current_reveal_step >= self._max_reveal_step:
            raise InteractionRuntimeError("reveal_exhausted", "No additional reveal steps remain for this slide.")
        self._current_reveal_step += 1
        return self.snapshot()

    def reset(self) -> SlideRuntimeSnapshot:
        self._current_reveal_step = 0
        self._selected_answer_index = None
        self._feedback_visible = False
        return self.snapshot()

    def select_answer(self, answer_index: int) -> SlideRuntimeSnapshot:
        if not self._supports_interaction("question_flow"):
            raise InteractionRuntimeError(
                "unsupported_event",
                "Answer selection is only supported for slides with question_flow interactions.",
            )
        if self._selected_answer_index is not None:
            raise InteractionRuntimeError("answer_already_selected", "This slide already has a selected answer.")
        if answer_index < 0 or answer_index >= self._answer_count:
            raise InteractionRuntimeError("invalid_answer_selection", "Selected answer index is out of range.")
        self._selected_answer_index = answer_index
        return self.snapshot()

    def reveal_feedback(self) -> SlideRuntimeSnapshot:
        if not self._supports_interaction("question_flow"):
            raise InteractionRuntimeError(
                "unsupported_event",
                "Feedback reveal is only supported for slides with question_flow interactions.",
            )
        if self._selected_answer_index is None:
            raise InteractionRuntimeError(
                "feedback_requires_answer",
                "Feedback cannot be revealed before an answer is selected.",
            )
        if self._feedback_visible:
            raise InteractionRuntimeError("feedback_already_visible", "Feedback is already visible for this slide.")

        self._feedback_visible = True
        feedback_steps = sorted(
            {
                block.reveal_step
                for block in self._slot_blocks("feedback")
                if block.reveal_step is not None
            }
        )
        if feedback_steps:
            self._current_reveal_step = max(self._current_reveal_step, feedback_steps[0])
        return self.snapshot()

    def _build_slot_visibility(self, slot_name: str, resolved_slot: ResolvedSlot) -> RuntimeSlotVisibility:
        visible_block_ids: list[str] = []
        hidden_block_ids: list[str] = []
        for block in resolved_slot.blocks:
            if self._is_block_visible(slot_name, block):
                visible_block_ids.append(block.block_id)
            else:
                hidden_block_ids.append(block.block_id)
        return RuntimeSlotVisibility(
            slot_name=slot_name,
            visible_block_ids=visible_block_ids,
            hidden_block_ids=hidden_block_ids,
        )

    def _is_block_visible(self, slot_name: str, block: Block) -> bool:
        reveal_ready = block.reveal_step is None or block.reveal_step <= self._current_reveal_step
        if slot_name == "feedback":
            return self._feedback_visible and reveal_ready
        return reveal_ready

    def _derive_active_mode(self) -> str:
        if self._feedback_visible:
            return "feedback"
        if self._supports_interaction("question_flow"):
            return "question"
        if self._max_reveal_step > 0:
            return "reveal"
        return "content"

    def _derive_answer_count(self) -> int:
        answer_slot = self._resolved_slide.slot_bindings.get("answer_choices")
        if answer_slot is None:
            return 0
        return sum(len(block.items) for block in answer_slot.blocks if block.kind == "list")

    def _validate_runtime_shape(self) -> None:
        interaction_kinds = {interaction.kind for interaction in self._resolved_slide.interactions}
        unsupported = sorted(interaction_kinds - SUPPORTED_INTERACTIONS)
        if unsupported:
            raise InteractionRuntimeError(
                "unsupported_runtime_shape",
                f"Unsupported interaction kinds for MVP runtime: {', '.join(unsupported)}",
            )

        if self._supports_interaction("question_flow"):
            required_slots = {"question", "answer_choices", "feedback"}
            missing = sorted(required_slots - self._resolved_slide.slot_bindings.keys())
            if missing:
                raise InteractionRuntimeError(
                    "incomplete_runtime_shape",
                    f"Question runtime requires slots: {', '.join(missing)}",
                )
            if self._answer_count <= 0:
                raise InteractionRuntimeError(
                    "incomplete_runtime_shape",
                    "Question runtime requires at least one authored answer choice.",
                )

    def _supports_interaction(self, interaction_kind: str) -> bool:
        return any(interaction.kind == interaction_kind for interaction in self._resolved_slide.interactions)

    def _slot_blocks(self, slot_name: str) -> list[Block]:
        slot = self._resolved_slide.slot_bindings.get(slot_name)
        if slot is None:
            return []
        return slot.blocks


def create_slide_runtime(resolved_slide: ResolvedTemplateSlide) -> SlideInteractionRuntime:
    return SlideInteractionRuntime(resolved_slide)