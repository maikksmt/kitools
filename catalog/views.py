from django.shortcuts import render, get_object_or_404
from .models import Tool, Category


def home(request):
    featured = Tool.objects.filter(is_featured=True)[:8]
    latest = Tool.objects.all()[:12]
    return render(request, 'catalog/home.html', {'featured': featured, 'latest': latest})


def tool_list(request):
    qs = Tool.objects.all().select_related()
    cat = request.GET.get('cat')
    if cat:
        qs = qs.filter(categories__slug=cat)
    return render(request, 'catalog/tool_list.html', {'tools': qs})


def tool_detail(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    return render(request, 'catalog/tool_detail.html', {'tool': tool})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tools = category.tools.all()
    return render(request, 'catalog/category_detail.html', {'category': category, 'tools': tools})
