
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
admin.site.site_header = "Stickify adminstration"
admin.site.site_title = "Stickify Admin"

urlpatterns = [
    path('stickify-admin-site/', admin.site.urls),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-docs-stickify', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("" , include('apps.urls')),
]


