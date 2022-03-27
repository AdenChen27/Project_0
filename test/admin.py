from django.contrib import admin
from test.models import *


class PassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'tags', 'author', 'counter', 'difficulty', )
    search_fields = ('title', 'author', 'tags', )
    ordering = ('difficulty', )


class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'lem_id', 'id', )
    search_fields = ('name', 'lem_id', )
    ordering = ('lem_id', )

class LemmaAdmin(admin.ModelAdmin):
    list_display = ('name', 'freq', 'id', 'def_en', 'def_zh', 'sent_ids', )
    search_fields = ('name', 'freq', 'id', )
    ordering = ('-freq', )

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('text', 'id', 'passage_id', )
    search_fields = ('text', 'id', 'passage_id', )
    ordering = ('text', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'password', )
    search_fields = ('first_name', 'last_name', )
    ordering = ('first_name', )

class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'counter', )


admin.site.register(Passage, PassageAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(SystemInfo, SystemInfoAdmin)
