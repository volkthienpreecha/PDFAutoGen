from __future__ import annotations

from random import Random

from pdf_autogenerator.content import load_snippet_bank
from pdf_autogenerator.models import PAGE_SIZE_POINTS, VariantChoices
from pdf_autogenerator.templates import TEMPLATES, build_document_plan


def _variant_for(template_id: str) -> VariantChoices:
    double_templates = {
        "lecture-handout",
        "reading-question-sheet",
        "practice-worksheet",
        "status-report",
        "course-syllabus",
        "program-information-sheet",
    }
    table_templates = {
        "status-report",
        "checklist-form",
        "invoice",
        "itemized-receipt",
        "course-syllabus",
        "program-information-sheet",
    }
    header_templates = {"invoice", "itemized-receipt"}
    return VariantChoices(
        page_size="letter",
        margin_preset="0.75in",
        density_preset="normal",
        font_key="source_serif_4",
        font_family="Source Serif 4",
        has_header=template_id in header_templates,
        has_footer=True,
        has_small_text=True,
        column_mode="double" if template_id in double_templates else "single",
        has_table_region=template_id in table_templates,
    )


def test_templates_expose_enough_legal_variants() -> None:
    for template in TEMPLATES:
        assert template.legal_variant_count() >= 4


def test_each_template_builds_non_empty_document_plan() -> None:
    bank = load_snippet_bank()
    for template in TEMPLATES:
        variant = _variant_for(template.template_id)
        plan = build_document_plan(template, variant, bank, PAGE_SIZE_POINTS["letter"], Random(template.template_id))
        assert plan.title
        assert plan.content_fingerprint
        assert any(region.blocks for region in plan.regions)
