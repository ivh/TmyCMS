from MyDjangoSites.blog.models import Tag,Entry
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ['title','body','slug']
    date_hierarchy = 'pub_date'
    list_filter = ['pub_date']

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name']



admin.site.register(Entry,EntryAdmin)
admin.site.register(Tag,TagAdmin)
