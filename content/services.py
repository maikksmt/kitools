# content/services.py
from __future__ import annotations
from typing import Any, Dict, List
from django.utils.translation import get_language

from catalog.models import Tool  # optional: falls du featured Tools später brauchst
from content.models import Guide, Prompt, UseCase


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
    Vereinheitlichter Teaser-Feed (Guides, Prompts, Use-Cases), nur published.
    Nutzt reale Felder aus deinem Projekt:
      - published Manager (Guide.published / Prompt.published / UseCase.published)
      - title, excerpt, slug, published_at
    """
    items: List[Dict[str, Any]] = []

    for obj in Guide.published.all().order_by("-published_at")[:limit]:
        items.append({
            "title": obj.title,
            "teaser": obj.excerpt,
            "url": f"/guides/{obj.slug}/",
            "date": obj.published_at,
            "badge": "Guide",
        })

    for obj in Prompt.published.all().order_by("-published_at")[:limit]:
        items.append({
            "title": obj.title,
            "teaser": obj.excerpt,
            "url": f"/prompts/{obj.slug}/",
            "date": obj.published_at,
            "badge": "Prompt",
        })

    for obj in UseCase.published.all().order_by("-published_at")[:limit]:
        items.append({
            "title": obj.title,
            "teaser": obj.problem[:180] if obj.problem else "",
            "url": f"/use-cases/{obj.slug}/",
            "date": obj.published_at,
            "badge": "Use-Case",
        })

    # Nach Datum sortieren und global begrenzen
    items.sort(key=lambda x: (x.get("date") or 0), reverse=True)
    return items[:limit]
