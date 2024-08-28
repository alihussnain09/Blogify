from django.contrib import admin
from . import models
from ckeditor.widgets import CKEditorWidget

admin.site.register(models.Tag)
admin.site.register(models.Category)
class Category(admin.ModelAdmin):
    list_filter = ('category',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display=('title','author','created _at')
    formfield_overrides = {
        models.RichTextField: {'widget': CKEditorWidget},
    }
admin.site.register(models.blog_post)
