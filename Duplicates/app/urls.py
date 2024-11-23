from django.urls import path, include

urlpatterns = [
    path('api/', include('backend.app.api.urls')),
]
