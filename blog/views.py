from django.http import Http404
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response,get_object_or_404
from simple_search import EntrySearchForm
from django.template import RequestContext

import logging
logging.basicConfig(filename='/tmp/mydjangodebug.log',level=logging.DEBUG)
l=logging.debug

def index(request,page=1):
    current_site = Site.objects.get_current()
    l(current_site.domain+'  ;  '+request.get_host())
    paginator = Paginator(Entry.objects.filter(site=current_site), 15)
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    return render_to_response('index.html', {"entries": entries})

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



class LatestEntriesFeed(Feed):
    title = Site.objects.get_current().name
    link = "http://%s"%Site.objects.get_current().domain
    description = ""

    def items(self):
        return Entry.objects.all()[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body


def search(request):
# from http://gregbrown.co.nz/code/django-simple-search/
    if request.GET:
        form = EntrySearchForm(request.GET)
        if form.is_valid():

            results = form.get_result_queryset()
        else:
            results = []
    else:
        form = EntrySearchForm()
        results = []


    return render_to_response(
        'search.html',
        RequestContext(request, {
            'form': form,
            'results': results,
        })
    )
