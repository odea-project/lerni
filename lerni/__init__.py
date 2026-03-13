from .document_model import Block, Deck, InteractionReference, Region, RevealGroup, Slide
from .parser import ParseError, parse_document
from .template_resolution import ResolvedSlot, ResolvedTemplateSlide, ResolutionIssue, TemplateResolutionError, resolve_deck_templates, resolve_slide_template

__all__ = [
    "Block",
    "Deck",
    "InteractionReference",
    "ParseError",
    "Region",
    "RevealGroup",
    "ResolvedSlot",
    "ResolvedTemplateSlide",
    "ResolutionIssue",
    "Slide",
    "TemplateResolutionError",
    "parse_document",
    "resolve_deck_templates",
    "resolve_slide_template",
]