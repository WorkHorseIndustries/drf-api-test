from django.conf.urls import patterns, include, url
from django.contrib import admin
from foo.views import FooList


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^foo/', FooList.as_view(), name='foo'),
)