from django.shortcuts import render, get_object_or_404
from .models import UseCase


def detail(request, slug):
    item = get_object_or_404(UseCase, slug=slug)
    return render(request, 'content/usecases/detail.html', {'item': item})
