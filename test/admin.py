from django.contrib import admin
from test.models import *


class PassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'tags', )
    search_fields = ('title', )
    ordering = ('title', )


class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'lem_id', 'id', )
    search_fields = ('name', 'lem_id', )
    ordering = ('lem_id', )

class LemmaAdmin(admin.ModelAdmin):
    list_display = ('name', 'freq', 'id', 'def_en', 'def_zh', )
    search_fields = ('name', 'freq', 'id', )
    ordering = ('-freq', )

class LemToSentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'sent_ids', )
    search_fields = ('name', 'id', 'sent_ids', )
    ordering = ('name', )

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('text', 'id', 'passage_id', )
    search_fields = ('text', 'id', 'passage_id', )
    ordering = ('text', )


admin.site.register(Passage, PassageAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Lemma, LemmaAdmin)
admin.site.register(LemToSent, LemToSentAdmin)
admin.site.register(Sentence, SentenceAdmin)
