from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Category, Post


def index(request):
    template = 'blog/index.html'

    # ✅ Добавьте [:5] в конце — ограничиваем до 5 постов
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

    context = {'post_list': posts}
    return render(request, template, context)


def category_posts(request, slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category=category,
        pub_date__lte=timezone.now()
    )
    context = {
        'category': category,
        'post_list': posts  # ✅ Ключ должен быть 'post_list'
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'location', 'author'
        ),
        pk=pk,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {'post': post}  # ✅ Ключ должен быть 'post'
    return render(request, template, context)
