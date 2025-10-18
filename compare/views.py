# compare/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.translation import gettext as _
from django.urls import reverse

from .models import Comparison
from catalog.models import Category


def index(request):
    """
    Übersicht aller Vergleiche mit optionalen Filtern.
    """
    qs = Comparison.objects.all().prefetch_related("tools", "tools__categories")

    q = request.GET.get("q")
    category = request.GET.get("category")

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(intro__icontains=q))
    if category:
        qs = qs.filter(tools__categories__slug=category)

    paginator = Paginator(qs.order_by("-id"), 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    available_categories = Category.objects.all().order_by("name")

    context = {
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "q": q or "",
        "category": category or "",
        "available_categories": available_categories,
        "title": _("Tool-Vergleiche"),
        "crumbs": [
            (_("Vergleiche"), request.path),
        ],
    }
    return render(request, "compare/index.html", context)


def detail(request, slug):
    """
    Detailansicht eines Vergleichs (inkl. Bewertungstabelle).
    """
    qs = (
        Comparison.objects
        .prefetch_related("tools", "tools__categories")
        # .select_related(...)  # nur falls du FKs auf winner o.ä. hast, sonst weglassen
    )
    obj = get_object_or_404(qs, slug=slug)

    # Kategorien aus den verknüpften Tools ableiten (unique, stabil)
    category_set = {}
    for tool in obj.tools.all():
        for cat in getattr(tool, "categories").all():
            category_set[cat.pk] = cat
    categories = list(category_set.values())

    # ---- score_breakdown für das Template vorbereiten ----
    # Erwartete Template-Struktur:
    #   tools_list: [Tool, Tool, ...] (Reihenfolge der Spalten)
    #   score_rows: [(criterion, [score_for_tool1, score_for_tool2, ...]), ...]
    tools_list = list(obj.tools.all())
    raw = obj.score_breakdown or {}
    score_rows = []

    for criterion, value in raw.items():
        per_tool = []
        if isinstance(value, dict):
            # Versuche verschiedene Keys (slug, name, pk, index) der Tools
            for idx, t in enumerate(tools_list):
                v = (
                        value.get(getattr(t, "slug", None))
                        or value.get(getattr(t, "name", None))
                        or value.get(str(getattr(t, "pk", "")))
                        or value.get(idx)  # falls numerisch indexiert
                        or value.get(str(idx))
                )
                per_tool.append(v if v not in (None, "") else "–")
        else:
            # z.B. "9 : 8" → splitten und nach Reihenfolge der Tools mappen
            parts = [s.strip() for s in str(value).split(":")]
            for idx, _t in enumerate(tools_list):
                per_tool.append(parts[idx] if idx < len(parts) else "–")

        score_rows.append((criterion, per_tool))

    # ähnliche Vergleiche: teilen sich mindestens ein Tool
    related = (
        Comparison.objects
        .prefetch_related("tools")
        .exclude(pk=obj.pk)
        .filter(tools__in=obj.tools.all())
        .annotate(shared_tools=Count("tools"))
        .order_by("-shared_tools", "title")
        .distinct()[:6]
    )

    context = {
        "object": obj,
        "categories": categories,  # ⟵ abgeleitete Kategorien
        "tools_list": tools_list,  # ⟵ für Tabellenkopf
        "score_rows": score_rows,  # ⟵ für Tabellenkörper
        "related": related,
        "title": obj.title,
        "crumbs": [(_("Vergleiche"), "/vergleiche/"), (obj.title, request.path)],
    }
    return render(request, "compare/detail.html", context)
