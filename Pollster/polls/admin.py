from django.contrib import admin
from .models import Question, Choice

# Change Admin site Header
admin.site.site_header = "Pollster App Admin"
admin.site.site_title = "Pollster App Admin Area"
admin.site.index_title = "Welcome to the Pollster App Admin"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        (
            "Date Information",
            {"fields": ["publication_date"], "classes": ["collapse"]},
        ),
    ]
    inlines = [ChoiceInLine]


# admin.site.register(Question)
# admin.site.register(Choice)


admin.site.register(Question, QuestionAdmin)
