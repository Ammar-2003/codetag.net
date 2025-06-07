from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView 
from django.core.cache import cache
from .models import Post
from .models import Post, Category, Tag
from django.views import View
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponse



class SearchPostsView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if query:
            search_terms = query.split()
            q_objects = Q()

            for term in search_terms:
                q_objects |= Q(title__icontains=term) | Q(content__icontains=term)

            posts = Post.objects.filter(q_objects).distinct()[:10]

            results = [
                {
                    'title': post.title,
                    'url': post.get_absolute_url(),
                    'excerpt': post.content[:100] + '...' if len(post.content) > 100 else post.content,
                }
                for post in posts
            ]

            return JsonResponse({'results': results})
        
        return JsonResponse({'results': []})

class PostListView(ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    paginate_by = 12 
    context_object_name = 'posts'
    ordering = '-published_at'  # Latest posts first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories and tags to context
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0)
        
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:10]
        
        return context

    def get_queryset(self):
        return Post.published.all().order_by('-published_at')
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.published.all()

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.status == 'published':
            post.increment_view_count()
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ No post_count logic — just fetch all categories
        context['categories'] = cache.get_or_set(
            'all_categories',
            Category.objects.all(),
            #60 * 60  # cache for 1 hour
        )

        return context

class CategoryPostListView(PostListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /preview/\n"
        "Disallow: /accounts/\n"
        "Sitemap: https://codetag.net/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")