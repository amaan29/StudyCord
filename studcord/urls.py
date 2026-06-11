
from django.contrib import admin
from django.urls import path, include
from django.conf import settings               #give access of settings
from django.conf.urls.static import static      # to import static method to store static files(images)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),   #anything with ...api/ at the end of its url gets sent to base.api.url file to handle it
]

urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    #connected media root to media URL