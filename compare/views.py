# compare/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
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
    obj = get_object_or_404(
        Comparison.objects.prefetch_related("tools", "categories"), slug=slug
    )

    # ähnliche Vergleiche nach Kategorie
    related_comparisons = (
        Comparison.objects.filter(categories__in=obj.categories.all())
        .exclude(pk=obj.pk)
        .distinct()
        .order_by("-id")[:6]
    )

    context = {
        "object": obj,
        "related_comparisons": related_comparisons,
        "title": obj.title,
        "crumbs": [
            (_("Vergleiche"),
             reverse("compare:index") if "compare:index" in request.resolver_match.namespaces else "/vergleiche/"),
            (obj.title, request.path),
        ],
    }
    return render(request, "compare/detail.html", context)
