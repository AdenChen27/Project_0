from django.contrib import admin
from test.models import Word, Lemma


# class PassageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'id', 'tags', )
#     search_fields = ('title', )
#     ordering = ('title', )


class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'lem_id', 'id', )
    search_fields = ('name', )
    ordering = ('lem_id', )

class LemmaAdmin(admin.ModelAdmin):
    list_display = ('name', 'freq', 'id', )
    search_fields = ('name', 'freq', 'id', )
    ordering = ('-freq', )


# class WordFreqAdmin(admin.ModelAdmin):
#     list_display = ('name', 'rank', 'id', )
#     search_fields = ('name', 'id', )
#     ordering = ('rank', ) 

# class WordDefAdmin(admin.ModelAdmin):
#     list_display = ('name', 'definition', 'id', )
#     search_fields = ('name', 'id', 'definition', )
#     ordering = ('name', )


# admin.site.register(Passage, PassageAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Lemma, LemmaAdmin)
# admin.site.register(WordFreq, WordFreqAdmin)
# admin.site.register(WordDef, WordDefAdmin)
