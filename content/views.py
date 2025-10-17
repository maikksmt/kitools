# content/views.py
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .services import get_homepage_cards, get_latest_items


class HomePageView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = _("KI Tools Web – Schneller Einstieg")
        ctx["seo_description"] = _("Finde Tools, vergleiche Alternativen und nutze praxisnahe Guides & Prompts.")
        ctx["entry_cards"] = get_homepage_cards()
        ctx["latest_items"] = get_latest_items(limit=6)
        return ctx
