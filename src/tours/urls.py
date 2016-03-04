from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.tour_list, name='tour_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.TourDetailView.as_view(), name='tour_detail'),
    url(r'service/(?P<pk>[0-9]+)/$', views.ServiceDetailView.as_view(), name='service_detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.tour_update, name='edit'),
    url(r'^contact/(?P<pk>[0-9]+)/edit/$', views.ContactEdit.as_view(), name='contact_edit'),

)
