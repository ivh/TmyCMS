from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry

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
    (r'^posts/', 'index'),
    (r'^post/(?P<id>\d+)/$','entry_by_id'),
    (r'^(?P<yr>\d{4})/(?P<mon>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$','entry_by_permalink'),
    (r'^tags/', 'tags'),
    (r'^tag/(?P<slug>\w+)/$','tag_view'),
 )

urlpatterns = adminpatterns + commentpatterns + entrypatterns
