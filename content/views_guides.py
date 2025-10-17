from django.shortcuts import render, get_object_or_404
from .models import Guide


def index(request):
    items = Guide.objects.all()
    return render(request, 'content/guides/index.html', {'items': items})


def detail(request, slug):
    item = get_object_or_404(Guide, slug=slug)
    return render(request, 'content/guides/detail.html', {'item': item})
