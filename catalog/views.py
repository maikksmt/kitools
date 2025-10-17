from django.shortcuts import render, get_object_or_404
from .models import Tool, Category


def home(request):
    featured = Tool.objects.filter(is_featured=True)[:8]
    latest = Tool.objects.all()[:12]
    return render(request, 'catalog/home.html', {'featured': featured, 'latest': latest})


def tool_list(request):
    qs = Tool.objects.all().prefetch_related('categories')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(short_desc__icontains=q)
    cat = request.GET.get('cat')
    if cat:
        qs = qs.filter(categories__slug=cat)
    category_list = Category.objects.all().order_by('name')
    return render(request, 'catalog/tool_list.html', {'tools': qs, 'category_list': category_list})


def tool_detail(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    return render(request, 'catalog/tool_detail.html', {'tool': tool})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tools = category.tools.all()
    return render(request, 'catalog/category_detail.html', {'category': category, 'tools': tools})
