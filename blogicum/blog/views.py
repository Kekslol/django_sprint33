from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category

# Вспомогательная функция для фильтрации опубликованных постов
def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('category', 'location', 'author')

def index(request):
    """Главная страница: 5 последних публикаций"""
    template = 'blog/index.html'
    # Берем 5 последних постов, удовлетворяющих условиям
    posts = get_published_posts()[:5]
    context = {
        'posts': posts,
    }
    return render(request, template, context)

def category_posts(request, slug):
    """Страница категории"""
    template = 'blog/category.html'
    
    # Получаем категорию. Если она не опубликована — сразу 404
    category = get_object_or_404(
        Category, 
        slug=slug, 
        is_published=True
    )
    
    # Фильтруем посты этой категории
    posts = get_published_posts().filter(category=category)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, template, context)

def post_detail(request, post_id):
    """Страница отдельной публикации"""
    template = 'blog/post_detail.html'
    
    # Получаем пост. Если он не опубликован, дата в будущем 
    # или категория не опубликована — вернется 404
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    
    context = {
        'post': post,
    }
    return render(request, template, context)