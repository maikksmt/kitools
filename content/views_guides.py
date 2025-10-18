# content/views_guides.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from .models import Guide
from .services import related_guides, to_teaser_item


def guide_list(request):
    """
    Zeigt nur veröffentlichte Guides.
    """
    qs = (
        Guide.published.all()
        .select_related("author")
        .prefetch_related("categories")
        .order_by("-published_at", "-updated_at")
    )

    paginator = Paginator(qs, 12)  # 12 Karten pro Seite
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        "page_obj": page_obj,
        "object_list": page_obj.object_list,  # für generische List-Templates
        "title": _("Guides"),
        "crumbs": [(_("Guides"), request.path)],
    }
    return render(request, "content/guides/list.html", ctx)


def guide_detail(request, slug):
    """
    Detailansicht nur für veröffentlichte Guides.
    Drafts sind nicht öffentlich erreichbar.
    """
    obj = get_object_or_404(Guide.published, slug=slug)

    # Verwandte Inhalte für Teaser / Weiterlesen
    related_qs = related_guides(obj, limit=6)
    related = [to_teaser_item(g, "guide") for g in related_qs]

    ctx = {
        "object": obj,
        "related": related,
        "title": obj.title,
        "crumbs": [(_("Guides"), "/guides/"), (obj.title, request.path)],
    }
    return render(request, "content/guides/detail.html", ctx)
