from django.contrib import admin
from tags.models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["label"]}
    search_fields = ["label"]


admin.site.register(TaggedItem)
