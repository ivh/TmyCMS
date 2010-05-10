from django.http import Http404
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry
from django.contrib.sites.models import Site

def entry_view(request, id):
    try:
        entry = Entry.objects.get(pk=id)
    except Entry.DoesNotExist:
        raise Http404
    
    return list_detail.object_detail(
        request,
        queryset = Entry.objects.all(),
        template_name = "entry.html",
        object_id=id
    )

def tag_view(request, slug):
    try:
        tag = Tag.objects.get(slug=slug)
    except Entry.DoesNotExist:
        raise Http404

    cursite=Site.objects.get_current()
    entries=tag.entries.filter(site=cursite)
    
    return list_detail.object_list(
        request,
        queryset = entries,
        template_name = "tag.html",
    )
