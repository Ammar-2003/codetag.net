from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.contrib.admin.models import LogEntry
from .models import Post, Category, Tag
from datetime import timezone

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['action_time', 'user', 'content_type']
    search_fields = ['user__username', 'object_repr', 'change_message']
    date_hierarchy = 'action_time'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'featured', 'post_count', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('featured',)
    list_filter = ('featured', 'created_at')

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_tutorial_tag', 'post_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    list_editable = ('is_tutorial_tag',)
    list_filter = ('is_tutorial_tag', 'created_at')

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'class': 'tinymce-editor'}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyMCE/tiny.js',)

    form = PostAdminForm
    list_display = (
        'title', 'status', 'post_type', 'featured', 'is_tutorial_series',
        'published_at', 'view_count', 'read_time', 'category', 'tag_list',
        'created_at', 'updated_at'
    )
    list_filter = (
        'status', 'post_type', 'featured', 'is_tutorial_series',
        'category', 'tags', 'published_at', 'created_at'
    )
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'view_count', 'created_at', 'updated_at', 'featured_image_preview',
        'read_time_display'
    )
    date_hierarchy = 'published_at'
    actions = ['make_published', 'make_draft', 'mark_as_featured', 'mark_as_tutorial']
    filter_horizontal = ('tags',)
    list_editable = ('featured', 'is_tutorial_series', 'post_type')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'status', 'post_type', 'published_at')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'featured_image_preview'),
            'classes': ('wide',)
        }),
        ('Taxonomy', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('Promotion', {
            'fields': ('featured', 'is_tutorial_series', 'tutorial_order'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'read_time', 'read_time_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 100%;" />', 
                obj.featured_image.url
            )
        return "No Image"
    featured_image_preview.short_description = 'Featured Image Preview'

    def read_time_display(self, obj):
        return f"{obj.read_time} min"
    read_time_display.short_description = 'Read Time'

    def tag_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()[:5]])
    tag_list.short_description = 'Tags'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    @admin.action(description="Mark selected posts as published")
    def make_published(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} posts were successfully published.')

    @admin.action(description="Mark selected posts as draft")
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts were successfully marked as draft.')

    @admin.action(description="Mark selected posts as featured")
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} posts were marked as featured.')

    @admin.action(description="Mark selected posts as tutorial series")
    def mark_as_tutorial(self, request, queryset):
        updated = queryset.update(is_tutorial_series=True, post_type='tutorial')
        self.message_user(request, f'{updated} posts were marked as tutorial series.')

admin.site.site_header = "Blog Administration"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to Blog Admin"