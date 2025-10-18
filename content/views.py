from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .services import get_homepage_cards, get_latest_items, related_guides, to_teaser_item
from .models import Guide


class HomePageView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = _("KI Tools Web – Schneller Einstieg")
        ctx["seo_description"] = _("Finde Tools, vergleiche Alternativen und nutze praxisnahe Guides & Prompts.")
        ctx["entry_cards"] = get_homepage_cards()
        ctx["latest_items"] = get_latest_items(limit=6)
        # Empfohlene Inhalte
        anchor = Guide.published.order_by("-published_at").first()
        ctx["recommended_items"] = [to_teaser_item(g, "guide") for g in
                                    related_guides(anchor, limit=3)] if anchor else []
        return ctx
