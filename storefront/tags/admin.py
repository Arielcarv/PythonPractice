from django.contrib import admin
from tags.models import Tag, TaggedItem

admin.site.regiter(Tag)
admin.site.regiter(TaggedItem)
