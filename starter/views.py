from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import StarterGuide


class StarterGuideView(TemplateView):
    template_name = "starter/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        guide = get_object_or_404(StarterGuide, slug="default", is_published=True)
        ctx["guide"] = guide
        return ctx


class StarterIntroView(TemplateView):
    template_name = "starter/intro.html"
