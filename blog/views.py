from django.http import Http404
from django.views.generic import list_detail
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response,get_object_or_404
from simple_search import EntrySearchForm
from django.template import RequestContext
from models import Tag,Entry

import logging
logging.basicConfig(filename='/tmp/mydjangodebug.log',level=logging.DEBUG)
L=logging.debug

def index(request,page=1):
    current_site = Site.objects.get_current()
    L(current_site.domain+'  ;  '+request.get_host())

    tags=Tag.objects.filter(site=current_site)

    paginator = Paginator(Entry.objects.filter(site=current_site), 15)
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    return render_to_response('index.html', {"entries": entries, 'tags':tags})

def tag_view(request, slug, page=1):
    tag = get_object_or_404(Tag,slug=slug)

    cursite=Site.objects.get_current()
    paginator = Paginator(tag.entries.filter(site=cursite),15)
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    return render_to_response('tag.html', {"entries": entries, 'tag':tag})


def tags(request):
    current_site = Site.objects.get_current()
    return list_detail.object_list(request,queryset=Tag.objects.filter(site=current_site), template_name='tags.html')

def entry_by_id(request, id):
    entry = get_object_or_404(Entry,pk=id)

    return list_detail.object_detail(
        request,
        queryset = Entry.objects.all(),
        template_name = "entry.html",
        object_id=id
    )

def entry_by_permalink(request, yr,mon,day,slug):
    entry = get_object_or_404(Entry,pub_date__year=yr, pub_date__month=mon,pub_date__day=day,slug=slug)

    return list_detail.object_detail(
        request,
        queryset = Entry.objects.all(),
        template_name = "entry.html",
        object_id=entry.id
    )


class LatestEntriesFeed(Feed):
    title = Site.objects.get_current().name
    link = "http://%s"%Site.objects.get_current().domain
    description = ""

    def items(self):
        return Entry.objects.filter(site=Site.objects.get_current())[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body.rendered


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
