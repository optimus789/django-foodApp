from django.contrib import auth
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [path('predict/', csrf_exempt(views.predict), name='predict')
               ] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
