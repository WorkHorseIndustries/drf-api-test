from django.conf.urls import patterns, include, url

from . import fake_api

urlpatterns = patterns('',
    url(
        r'^fake/?$',
        fake_api.FakeListCreateView.as_view(),
        name="fake_list"
    ),
    url(
        r'^fake/(?P<pk>\d+)/?$',
        fake_api.FakeRetrieveUpdateDeleteView.as_view(),
        name="fake_detail"
    ),
)
