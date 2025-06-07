from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published', published_at__lte=timezone.now())


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False, help_text="Mark this category as featured on homepage")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_tutorial_tag = models.BooleanField(
        default=False,
        help_text="Mark this tag as tutorial-related (e.g., 'django', 'python')"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    POST_TYPE_CHOICES = [
        ('regular', 'Regular Post'),
        ('tutorial', 'Tutorial'),
        ('story', 'Behind the Code Story'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, max_length=300)
    featured_image = models.ImageField(upload_to='blog/featured_images/%Y/%m/%d/', blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Post classification fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default='regular',
        help_text="Classification for different post types"
    )
    
    # Status and publication fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Visibility and promotion fields
    featured = models.BooleanField(
        default=False,
        help_text="Mark this post as featured (will appear in featured section)"
    )
    is_tutorial_series = models.BooleanField(
        default=False,
        help_text="Is this part of a tutorial series?"
    )
    tutorial_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in tutorial series (lower numbers come first)"
    )
    
    # Engagement metrics
    view_count = models.PositiveIntegerField(default=0, editable=False)
    read_time = models.PositiveIntegerField(
        default=0,
        help_text="Estimated read time in minutes"
    )

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager for published posts

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['featured']),
            models.Index(fields=['post_type']),
            models.Index(fields=['tutorial_order']),
        ]
        get_latest_by = ['published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # Auto-calculate read time if not set (approx 200 words per minute)
        if not self.read_time and self.content:
            word_count = len(self.content.split())
            self.read_time = max(1, round(word_count / 200))
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.published_at:
            return reverse('blog:post_preview', kwargs={'slug': self.slug})
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def is_tutorial(self):
        return self.post_type == 'tutorial' or self.tags.filter(is_tutorial_tag=True).exists()

    @property
    def is_story(self):
        return self.post_type == 'story' or self.tags.filter(name__in=['personal', 'journey', 'story']).exists()