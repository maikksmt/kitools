# catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _
from django.urls import reverse

from .models import Tool, Category


def home(request):
    """
    Startseite für den Tool-Katalog.
    Zeigt eine Auswahl an Tools (z. B. nach Bewertung, Kategorie oder Zufall).
    """
    featured_qs = Tool.objects.filter(is_featured=True)
    if featured_qs.exists():
        featured_tools = featured_qs.order_by("-published_at")[:6]
    else:
        featured_tools = Tool.objects.all().order_by("-published_at")[:6]

    context = {
        "featured_tools": featured_tools,
        "title": _("KI-Tool Katalog"),
        "crumbs": [
            (_("Katalog"), request.path),
        ],
    }
    return render(request, "catalog/home.html", context)


def tool_list(request):
    """
    Listet alle Tools mit Filter- und Suchoptionen.
    """
    qs = Tool.objects.all().prefetch_related("categories")

    # Filter: Suchbegriff, Sprache, Free-Tier
    q = request.GET.get("q")
    language = request.GET.get("language")
    free = request.GET.get("free")

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(short_desc__icontains=q) | Q(long_desc__icontains=q))
    if language:
        qs = qs.filter(language_support__icontains=language)
    if free:
        qs = qs.filter(free_tier=True)

    # Pagination
    paginator = Paginator(qs.order_by("name"), 18)
    page_obj = paginator.get_page(request.GET.get("page"))

    # verfügbare Sprachen (optional dynamisch aus DB aggregieren)
    available_languages = ["DE", "EN", "FR", "ES"]

    context = {
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "q": q or "",
        "language": language or "",
        "free": bool(free),
        "available_languages": available_languages,
        "title": _("Alle Tools"),
        "crumbs": [
            (_("Katalog"),
             reverse("catalog:tool_list") if "catalog:tool_list" in request.resolver_match.namespaces else "/"),
            (_("Alle Tools"), request.path),
        ],
    }
    return render(request, "catalog/tool_list.html", context)


def tool_detail(request, slug):
    """
    Zeigt die Detailansicht eines Tools inklusive verwandter Tools.
    """
    obj = get_object_or_404(
        Tool.objects.prefetch_related("categories"), slug=slug
    )

    # Ähnliche Tools (nach Kategorien)
    related_tools = (
        Tool.objects.filter(categories__in=obj.categories.all())
        .exclude(pk=obj.pk)
        .distinct()
        .order_by("-published_at")[:6]
    )

    context = {
        "object": obj,
        "related_tools": related_tools,
        "title": obj.name,
        "crumbs": [
            (_("Katalog"), reverse("catalog:tool_list")),
            (_("Alle Tools"), reverse("catalog:tool_list")),
            (obj.name, request.path),
        ],
    }
    return render(request, "catalog/tool_detail.html", context)
