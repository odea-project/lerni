# Template Resolution MVP

The first executable template-resolution slice is intentionally narrow. It consumes normalized `Slide` objects from the parser, selects a supported template contract, validates semantic regions against declared slots, and returns a resolved structural mapping for downstream runtime work.

## Supported Contracts

- `title-overview`
  - supported slide kind: `overview`
  - required slots: `title`, `explanation`
  - optional slots: `example`
- `quiz-feedback`
  - supported slide kind: `quiz`
  - required slots: `title`, `question`, `answer_choices`, `feedback`

## Selection Rules

- an explicit slide template is used when present
- otherwise the resolver falls back to a documented default by slide kind
- unsupported templates or unsupported slide-kind combinations fail immediately

## Validation Rules

- required slots must be present
- optional slots may be omitted and are reported in the resolved output
- regions not declared by the selected template fail resolution
- slot content must use block kinds allowed by the contract
- the resolver does not coerce invalid structures into alternative layouts

## Output Shape

Successful resolution returns a `ResolvedTemplateSlide` that records:

- selected template identity
- resolved slot bindings by slot name
- omitted optional slots
- reveal groups copied from the normalized slide
- interaction references copied from the normalized slide

The output is structural only. It does not choose a renderer, apply styling, or execute runtime interaction behavior.