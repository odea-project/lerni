from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .interaction_runtime import create_slide_runtime
from .parser import parse_document
from .template_resolution import resolve_deck_templates


def build_browser_payload_from_source(source: str, deck_id: str = "deck-1") -> dict[str, object]:
    deck = parse_document(source, deck_id=deck_id)
    resolved_slides = resolve_deck_templates(deck)
    return {
        "deckId": deck.deck_id,
        "slides": [
            _serialize_resolved_slide(resolved_slide)
            for resolved_slide in resolved_slides
        ],
    }


def write_browser_payload(source_path: Path, output_path: Path, deck_id: str = "deck-1") -> Path:
    payload = build_browser_payload_from_source(source_path.read_text(encoding="utf-8"), deck_id=deck_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def _serialize_resolved_slide(resolved_slide) -> dict[str, object]:
    runtime = create_slide_runtime(resolved_slide)
    initial_snapshot = runtime.snapshot()
    answer_slot = resolved_slide.slot_bindings.get("answer_choices")
    answer_count = 0
    if answer_slot is not None:
        answer_count = sum(len(block.items) for block in answer_slot.blocks if block.kind == "list")

    return {
        "slideId": resolved_slide.slide_id,
        "templateId": resolved_slide.template_id,
        "slideKind": resolved_slide.slide_kind,
        "slotSequence": list(resolved_slide.slot_bindings.keys()),
        "slots": [
            {
                "slotName": slot_name,
                "regionName": resolved_slot.region_name,
                "blocks": [asdict(block) for block in resolved_slot.blocks],
            }
            for slot_name, resolved_slot in resolved_slide.slot_bindings.items()
        ],
        "interactions": [interaction.kind for interaction in resolved_slide.interactions],
        "runtime": {
            "maxRevealStep": initial_snapshot.max_reveal_step,
            "answerCount": answer_count,
            "initialSnapshot": _serialize_snapshot(initial_snapshot),
        },
    }


def _serialize_snapshot(snapshot) -> dict[str, object]:
    return {
        "slideId": snapshot.slide_id,
        "templateId": snapshot.template_id,
        "currentRevealStep": snapshot.current_reveal_step,
        "maxRevealStep": snapshot.max_reveal_step,
        "canAdvanceReveal": snapshot.can_advance_reveal,
        "selectedAnswerIndex": snapshot.selected_answer_index,
        "feedbackVisible": snapshot.feedback_visible,
        "activeMode": snapshot.active_mode,
        "slotVisibility": {
            slot_name: {
                "slotName": visibility.slot_name,
                "visibleBlockIds": visibility.visible_block_ids,
                "hiddenBlockIds": visibility.hidden_block_ids,
            }
            for slot_name, visibility in snapshot.slot_visibility.items()
        },
    }