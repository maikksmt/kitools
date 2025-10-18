"""
URL configuration for kitools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from content.sitemaps import GuideSitemap, PromptSitemap, UseCaseSitemap
from catalog.sitemaps import ToolSitemap
from compare.sitemaps import ComparisonSitemap
from content.views import SetLevelView

sitemaps = {
    "guides": GuideSitemap,
    "prompts": PromptSitemap,
    "usecases": UseCaseSitemap,
    "tools": ToolSitemap,
    "comparisons": ComparisonSitemap,
}

urlpatterns = [
    path("i18n/setlang/", set_language, name="set_language"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include(("content.urls", "content"), namespace="content")),
    path("set-level/", SetLevelView.as_view(), name="set_level"),
    path("tools/", include("catalog.urls")),  # Home & Tools
    path("guides/", include("content.urls_guides")),
    path("prompts/", include("content.urls_prompts")),
    path("use-cases/", include("content.urls_usecases")),
    path("compare/", include("compare.urls")),
    path("newsletter/", include("newsletter.urls")),
    path("starter-guide/", include(("starter.urls", "starter"), namespace="starter")),
    # path("api/", include("api.urls")),
)

urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
        name="robots_txt",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
