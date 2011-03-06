from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
              (r'^admin/doc/', include('django.contrib.admindocs.urls')),
              (r'^admin/', include(admin.site.urls)),
              (r'^comments/', include('django.contrib.comments.urls')),
)


urlpatterns += patterns('',
    (r'', include('blog.urls')),
    )
