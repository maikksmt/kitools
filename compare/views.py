from django.shortcuts import render, get_object_or_404
from .models import Comparison


def index(request):
    items = Comparison.objects.all()
    return render(request, 'compare/index.html', {'items': items})


def detail(request, slug):
    cmp = get_object_or_404(Comparison, slug=slug)
    return render(request, 'compare/detail.html', {'cmp': cmp})
