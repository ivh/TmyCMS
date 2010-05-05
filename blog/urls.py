from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed


feeds = {
    'latest': LatestCommentFeed,
}

urlpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

)
