from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from diary import views
from django.conf.urls import include

urlpatterns = [
    url(r'^entries/$', views.EntryList.as_view()),
    url(r'^entries/(?P<pk>[0-9]+)$', views.EntryDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^register/$', views.UserView.as_view({'post': 'create'})),
    url(r'^login/$', views.LoginView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
