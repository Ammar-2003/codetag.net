# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Post
from django.utils import timezone

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(published_at__lte=timezone.now())  # only published blogs

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()