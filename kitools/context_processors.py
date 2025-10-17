from django.conf import settings


def seo_site(request):
    """
    Liefert SITE_NAME und SITE_URL in jedes Template.
    """
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Website"),
        "SITE_URL": getattr(settings, "SITE_URL", ""),
    }
