from django.http import Http404
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry
from django.contrib.sites.models import Site


def index(request):
    current_site = Site.objects.get_current()
    return list_detail.object_list(request,queryset=Entry.objects.filter(site=current_site)[:15], template_name='index.html')

def tags(request):
    current_site = Site.objects.get_current()
    return list_detail.object_list(request,queryset=Tag.objects.filter(site=current_site), template_name='tags.html')

def entry_by_id(request, id):
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

def entry_by_permalink(request, yr,mon,day,slug):
    try:
        entry = Entry.objects.get(pub_date__year=yr, pub_date__month=mon,pub_date__day=day,slug=slug)
    except Entry.DoesNotExist:
        raise Http404
    
    return list_detail.object_detail(
        request,
        queryset = Entry.objects.all(),
        template_name = "entry.html",
        object_id=entry.id
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
