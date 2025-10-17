from django.shortcuts import render, get_object_or_404
from .models import Prompt


def index(request):
    items = Prompt.objects.all()
    return render(request, 'content/prompts/index.html', {'items': items})


def detail(request, slug):
    item = get_object_or_404(Prompt, slug=slug)
    return render(request, 'content/prompts/detail.html', {'item': item})
