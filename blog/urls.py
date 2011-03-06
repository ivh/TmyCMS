from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed
from models import Tag,Entry
from views import LatestEntriesFeed

feeds = {
    'comments': LatestCommentFeed,
    'posts':LatestEntriesFeed,
}

urlpatterns = patterns('',
    (r'^comments/feed/', LatestCommentFeed()),
    (r'^feed/',LatestEntriesFeed()),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('blog.views',
    (r'^$', 'index'),
    url(r'^page/(?P<page>\d+)/$', 'index',name='pindex'),
    url(r'^(?P<yr>\d{4})/(?P<mon>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$','entry_by_permalink',name='permalink'),
    (r'^tags/$', 'tags'),
    url(r'^tag/(?P<slug>\w+)/$','tag_view',name='tag'),
    url(r'^tag/(?P<slug>\w+)/page/(?P<page>\d+)/$','tag_view',name='tagpage'),
    (r'^post/(?P<id>\d+)/$','entry_by_id'),
    url(r'^search/$','search',name='search'),

 )
