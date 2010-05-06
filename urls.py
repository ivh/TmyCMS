from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry

from django.contrib.sites.models import Site
current_site = Site.objects.get_current()

from django.contrib import admin
admin.autodiscover()

adminpatterns = patterns('',
              (r'^admin/doc/', include('django.contrib.admindocs.urls')),
              (r'^admin/', include(admin.site.urls)),
)


feeds = {
    'latest': LatestCommentFeed,
}

commentpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

)

entrypatterns = patterns('MyDjangoSites.blog.views',
                         (r'^posts/', list_detail.object_list, {'queryset':Entry.objects.all(),
                                                                'template_name':'index.html'
                                                                }),
                         (r'^post/(?P<id>\d+)/$','entry_view'),
                         (r'^tags/', list_detail.object_list, {'queryset':Tag.objects.all(),
                                                                'template_name':'tags.html'
                                                                }),
                         (r'^tag/(?P<slug>\w+)/$','tag_view'),
  
 )

urlpatterns = adminpatterns + commentpatterns + entrypatterns
