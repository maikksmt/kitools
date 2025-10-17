# content/views_prompts.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from .models import Prompt


def prompt_list(request):
    """
    Zeigt nur veröffentlichte Prompts.
    Optional: einfache Textsuche über ?q=
    """
    qs = (
        Prompt.published.all()
        .select_related("author")
        .prefetch_related("tools", "tags")
        .order_by("-published_at", "-updated_at")
    )

    q = request.GET.get("q")
    if q:
        # schnell & simpel; später auf Search umstellen
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, 18)  # 18 Karten pro Seite
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "q": q or "",
        "title": _("Prompts"),
        "crumbs": [(_("Prompts"), request.path)],
    }
    return render(request, "content/prompts/list.html", ctx)


def prompt_detail(request, slug):
    """
    Detailansicht nur für veröffentlichte Prompts.
    """
    obj = get_object_or_404(Prompt.published, slug=slug)

    # (Optional) weitere Prompts zum Weiterlesen
    more = (
        Prompt.published.exclude(pk=obj.pk)
        .prefetch_related("tags")
        .order_by("-published_at")[:8]
    )

    ctx = {
        "object": obj,
        "more": more,
        "title": obj.title,
        "crumbs": [(_("Prompts"), "/prompts/"), (obj.title, request.path)],
    }
    return render(request, "content/prompts/detail.html", ctx)
