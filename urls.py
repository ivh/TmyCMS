from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import list_detail
from MyDjangoSites.blog.models import Tag,Entry
from MyDjangoSites.blog.views import LatestEntriesFeed


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
              (r'^admin/doc/', include('django.contrib.admindocs.urls')),
              (r'^admin/', include(admin.site.urls)),
              (r'^comments/', include('django.contrib.comments.urls')),
)


feeds = {
    'comments': LatestCommentFeed,
    'posts':LatestEntriesFeed,
}

urlpatterns += patterns('',
    (r'^comments/feed/', LatestCommentFeed()),
    (r'^feed/',LatestEntriesFeed()),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('MyDjangoSites.blog.views',
    (r'^$', 'index'),
    url(r'^(?P<yr>\d{4})/(?P<mon>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$','entry_by_permalink',name='permalink'),
    (r'^tags/$', 'tags'),
    url(r'^tag/(?P<slug>\w+)/$','tag_view',name='tag'),
    (r'^post/(?P<id>\d+)/$','entry_by_id'),
    
 )
