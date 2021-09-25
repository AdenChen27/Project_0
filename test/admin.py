from django.contrib import admin
from test.models import Passage, Word, WordFreq, WordDef


class PassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'tags', )
    search_fields = ('title', )
    ordering = ('title', )


class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'p_id', 'select_cnt', 'def_id', 'id', )
    search_fields = ('name', 'id', )
    ordering = ('p_id', )
    list_filter = ("p_id", )


class WordFreqAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'id', )
    search_fields = ('name', 'id', )
    ordering = ('rank', )

class WordDefAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition', 'id', )
    search_fields = ('name', 'id', 'definition', )
    ordering = ('name', )


admin.site.register(Passage, PassageAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(WordFreq, WordFreqAdmin)
admin.site.register(WordDef, WordDefAdmin)
