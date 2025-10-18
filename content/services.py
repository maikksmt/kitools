# content/services.py
from __future__ import annotations
from typing import Any, Dict, List
from django.utils.translation import get_language
from django.utils.html import strip_tags
from django.db.models import Count, Q
from content.models import Guide, Prompt, UseCase
from django.urls import reverse


# ---------- kleine Helfer ----------

def _safe_order_by_published(qs):
    """Falls ein Modell (oder DB) published_at (noch) nicht hat, fallback auf -id."""
    try:
        # trigger SQL compile to catch missing column early
        str(qs.order_by("-published_at").query)
        return qs.order_by("-published_at")
    except Exception:
        return qs.order_by("-id")


def _first(seq):
    try:
        return next(iter(seq)) if seq else ""
    except Exception:
        return ""


def teaser_for_guide(g: Guide, limit: int = 160) -> str:
    src = getattr(g, "excerpt", None) or getattr(g, "body", "") or ""
    return (strip_tags(src) or "")[:limit]


def teaser_for_prompt(p: Prompt, limit: int = 160) -> str:
    # bevorzugt Beispiel, sonst body
    ex = ""
    examples = getattr(p, "examples", None)
    if isinstance(examples, (list, tuple)):
        ex = _first(examples)
    elif isinstance(examples, str):
        ex = examples
    src = ex or getattr(p, "body", "") or ""
    return (strip_tags(src) or "")[:limit]


def teaser_for_usecase(u: UseCase, limit: int = 160) -> str:
    steps = getattr(u, "workflow_steps", None)
    step0 = _first(steps) if isinstance(steps, (list, tuple)) else ""
    src = getattr(u, "problem", "") or step0 or ""
    return (strip_tags(src) or "")[:limit]


def to_teaser_item(obj, kind: str) -> Dict[str, Any]:
    if kind == "guide":
        return {
            "title": obj.title,
            "teaser": teaser_for_guide(obj),
            "url": reverse("guides:detail", kwargs={"slug": obj.slug}),
            "date": getattr(obj, "published_at", None),
            "badge": "Guide",
        }
    if kind == "prompt":
        return {
            "title": obj.title,
            "teaser": teaser_for_prompt(obj),
            "url": reverse("prompts:detail", kwargs={"slug": obj.slug}),
            "date": getattr(obj, "published_at", None),
            "badge": "Prompt",
        }
    if kind == "usecase":
        return {
            "title": obj.title,
            "teaser": teaser_for_usecase(obj),
            "url": reverse("usecases:detail", kwargs={"slug": obj.slug}),
            "date": getattr(obj, "published_at", None),
            "badge": "Use-Case",
        }
    return {"title": str(obj), "teaser": "", "url": "#", "date": None, "badge": kind.title()}


def get_homepage_cards(lang: str | None = None) -> List[Dict[str, Any]]:
    lang = lang or get_language() or "de"
    de = lang.startswith("de")

    if de:
        return [
            {"title": "Tool-Katalog", "desc": "Finde passende KI-Tools nach Kategorie.", "href": "/tools/",
             "icon": ("solid", "squares-2x2")},
            {"title": "Vergleiche", "desc": "Direkte Gegenüberstellungen der besten Tools.", "href": "/vergleiche/",
             "icon": ("solid", "adjustments-vertical")},
            {"title": "Guides", "desc": "Schritt-für-Schritt-Anleitungen aus der Praxis.", "href": "/guides/",
             "icon": ("solid", "book-open")},
            {"title": "Prompts", "desc": "Sofort nutzbare Prompt-Vorlagen.", "href": "/prompts/",
             "icon": ("solid", "sparkles")},
            {"title": "Use-Cases", "desc": "Konkrete Anwendungsfälle mit Workflows.", "href": "/use-cases/",
             "icon": ("solid", "briefcase")},
            # {"title": "Newsletter", "desc": "Monatliches KI-Update.", "href": "/newsletter/", "icon": ("solid", "envelope")},  # optional
        ]
    else:
        return [
            {"title": "Tool Catalog", "desc": "Find AI tools by category.", "href": "/tools/",
             "icon": ("solid", "squares-2x2")},
            {"title": "Comparisons", "desc": "Head-to-head tool comparisons.", "href": "/vergleiche/",
             "icon": ("solid", "adjustments-vertical")},
            {"title": "Guides", "desc": "Hands-on, step-by-step guides.", "href": "/guides/",
             "icon": ("solid", "book-open")},
            {"title": "Prompts", "desc": "Ready-to-use prompt templates.", "href": "/prompts/",
             "icon": ("solid", "sparkles")},
            {"title": "Use Cases", "desc": "Concrete workflows and outcomes.", "href": "/use-cases/",
             "icon": ("solid", "briefcase")},
            # {"title": "Newsletter", "desc": "Monthly digest.", "href": "/newsletter/", "icon": ("solid", "envelope")},
        ]


def get_latest_items(limit: int = 6) -> List[Dict[str, Any]]:
    """
    Neueste veröffentlichte Inhalte (Guides, Prompts, Use-Cases) – robust gegenüber fehlenden Feldern.
    """
    items: List[Dict[str, Any]] = []

    # Guides
    g_qs = _safe_order_by_published(Guide.published.all())
    for g in g_qs[:limit]:
        items.append(to_teaser_item(g, "guide"))

    # Prompts (kein excerpt-Feld -> eigener Teaser)
    p_qs = _safe_order_by_published(Prompt.published.all())
    for p in p_qs[:limit]:
        items.append(to_teaser_item(p, "prompt"))

    # UseCases
    u_qs = _safe_order_by_published(UseCase.published.all())
    for u in u_qs[:limit]:
        items.append(to_teaser_item(u, "usecase"))

    # global sortieren & kappen
    items.sort(key=lambda x: (x.get("date") or 0), reverse=True)
    return items[:limit]


def _ids(qs, field="id"):
    return list(qs.values_list(field, flat=True))


def related_guides(guide, limit=6):
    """
    Relevanz: gemeinsame Kategorien + gemeinsame Tools.
    Falls nichts passt: Fallback auf zeitlich nahe Guides.
    """
    cat_ids = _ids(guide.categories.all()) if hasattr(guide, "categories") else []
    tool_ids = _ids(guide.related_tools.all()) if hasattr(guide, "related_tools") else []

    qs = (
        Guide.published.exclude(pk=guide.pk)
        .prefetch_related("categories", "related_tools")
    )

    # Score via Matches (Kategorien + Tools)
    qs = (
        qs.filter(
            Q(categories__in=cat_ids) | Q(related_tools__in=tool_ids)
        )
        .annotate(
            cat_matches=Count("categories", filter=Q(categories__in=cat_ids), distinct=True),
            tool_matches=Count("related_tools", filter=Q(related_tools__in=tool_ids), distinct=True),
        )
        .annotate(score=Count("id"))  # Dummy, um ORDER BY zu erlauben
        .order_by("-cat_matches", "-tool_matches", "-published_at")
    )

    items = list(qs[:limit])
    if len(items) < limit:
        # Fallback ergänzen (ohne harte Duplikate)
        fallback = (
            Guide.published.exclude(pk__in=[g.pk for g in items] + [guide.pk])
            .order_by("-published_at")[: limit - len(items)]
        )
        items.extend(fallback)
    return items[:limit]


def related_prompts(prompt, limit=8):
    """
    Relevanz: gemeinsame Tags + gemeinsame Tools.
    Fallback: jüngste Prompts.
    """
    tag_ids = _ids(prompt.tags.all()) if hasattr(prompt, "tags") else []
    tool_ids = _ids(prompt.tools.all()) if hasattr(prompt, "tools") else []

    qs = (
        Prompt.published.exclude(pk=prompt.pk)
        .prefetch_related("tags", "tools")
    )

    if tag_ids or tool_ids:
        qs = (
            qs.filter(Q(tags__in=tag_ids) | Q(tools__in=tool_ids))
            .annotate(
                tag_matches=Count("tags", filter=Q(tags__in=tag_ids), distinct=True),
                tool_matches=Count("tools", filter=Q(tools__in=tool_ids), distinct=True),
            )
            .order_by("-tag_matches", "-tool_matches", "-published_at")
        )
    else:
        qs = qs.order_by("-published_at")

    items = list(qs[:limit])
    if len(items) < limit:
        fallback = (
            Prompt.published.exclude(pk__in=[p.pk for p in items] + [prompt.pk])
            .order_by("-published_at")[: limit - len(items)]
        )
        items.extend(fallback)
    return items[:limit]


def related_usecases(usecase, limit=6):
    """
    Relevanz: gleiche Persona + gemeinsame Tools.
    Fallback: jüngste Use-Cases.
    """
    persona = getattr(usecase, "persona", "") or ""
    tool_ids = _ids(usecase.tools.all()) if hasattr(usecase, "tools") else []

    qs = (
        UseCase.published.exclude(pk=usecase.pk)
        .prefetch_related("tools")
    )

    persona_q = Q()
    if persona:
        persona_q = Q(persona__iexact=persona)

    if persona or tool_ids:
        qs = (
            qs.filter(persona_q | Q(tools__in=tool_ids))
            .annotate(
                persona_match=Count("id", filter=Q(persona__iexact=persona)),
                tool_matches=Count("tools", filter=Q(tools__in=tool_ids), distinct=True),
            )
            .order_by("-persona_match", "-tool_matches", "-published_at")
        )
    else:
        qs = qs.order_by("-published_at")

    items = list(qs[:limit])
    if len(items) < limit:
        fallback = (
            UseCase.published.exclude(pk__in=[u.pk for u in items] + [usecase.pk])
            .order_by("-published_at")[: limit - len(items)]
        )
        items.extend(fallback)
    return items[:limit]
