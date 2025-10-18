from django.views.generic import TemplateView, View
from django.utils.translation import gettext_lazy as _
from .services import get_homepage_cards, get_latest_items, related_guides, to_teaser_item
from .models import Guide, Tool
from django.http import HttpResponseRedirect
from django.urls import reverse

LEVEL_COOKIE = "ktw_level"


class SetLevelView(View):
    def post(self, request):
        level = request.POST.get("level", "starter")
        resp = HttpResponseRedirect(request.POST.get("next") or "/")
        resp.set_cookie("ktw_level", level, max_age=60 * 60 * 24 * 180, samesite="Lax")
        return resp


class HomePageView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = _("KI Tools Web – Schneller Einstieg")
        ctx["entry_cards"] = get_homepage_cards()
        ctx["latest_items"] = get_latest_items(limit=6)
        ctx["featured_tools"] = Tool.objects.filter(is_featured=True).order_by("-published_at")[:6]
        # Personalisiert empfohlene Inhalte
        anchor = Guide.published.order_by("-published_at").first()
        ctx["recommended_items"] = [to_teaser_item(g, "guide") for g in
                                    related_guides(anchor, limit=3)] if anchor else []
        return ctx
