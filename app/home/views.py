from django.views.generic import TemplateView
from app.blog.models import Post 
from django.views.generic import TemplateView
from app.blog.models import Post 
from django.utils import timezone

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get top 3 most viewed published posts
        top_posts = Post.published.all().order_by('-view_count')[:9]
        context['top_posts'] = top_posts
        
        # Get featured post - first try explicitly featured, then fallback
        featured_post = Post.published.filter(featured=True).first()
        if not featured_post:
            featured_post = Post.published.order_by('-view_count').first()
        context['featured_post'] = featured_post
             
        # Get behind the code stories
        behind_code_posts = Post.published.filter(post_type='story').order_by('-published_at')[:3]
        if behind_code_posts.count() < 3:
            remaining = 3 - behind_code_posts.count()
            story_posts = Post.published.filter(tags__name__in=['personal', 'journey']).exclude(id__in=[p.id for p in behind_code_posts])[:remaining]
            behind_code_posts = list(behind_code_posts) + list(story_posts)
        context['behind_code_posts'] = behind_code_posts
        
        return context