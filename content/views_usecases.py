# content/views_usecases.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from .models import UseCase


def usecase_list(request):
    """
    Zeigt nur veröffentlichte Use-Cases.
    Optional: Filter nach Persona via ?persona=...
    """
    qs = (
        UseCase.published.all()
        .select_related("author")
        .prefetch_related("tools")
        .order_by("-published_at", "-updated_at")
    )

    persona = request.GET.get("persona")
    if persona:
        qs = qs.filter(persona__iexact=persona)

    paginator = Paginator(qs, 12)  # 12 Karten pro Seite
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "persona": persona or "",
        "title": _("Anwendungsfälle"),
        "crumbs": [(_("Anwendungsfälle"), request.path)],
    }
    return render(request, "content/usecases/list.html", ctx)


def usecase_detail(request, slug):
    """
    Detailansicht nur für veröffentlichte Use-Cases.
    """
    obj = get_object_or_404(UseCase.published, slug=slug)

    # (Optional) ähnliche Cases anhand Persona
    similar = (
        UseCase.published.exclude(pk=obj.pk)
        .filter(persona__iexact=obj.persona)
        .order_by("-published_at")[:6]
    )

    ctx = {
        "object": obj,
        "similar": similar,
        "title": obj.title,
        "crumbs": [(_("Anwendungsfälle"), "/use-cases/"), (obj.title, request.path)],
    }
    return render(request, "content/usecases/detail.html", ctx)
