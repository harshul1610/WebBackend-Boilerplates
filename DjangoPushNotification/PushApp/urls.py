from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home),
    url(r'^serviceworker.js', views.ServiceWorkerView.as_view()),
    url(r'^saveinformation', views.SaveInformation),
    url(r'^sendnotification', views.SendNotification)
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)