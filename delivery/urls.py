from django.urls import path, include

urlpatterns = [
    path('api/', include('delivery_api.main.router')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
