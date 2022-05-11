from django.contrib import admin
from django.urls import path
from .views import index
from accounts.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('accounts/login/', login_view),
    path('logout', logout_view)
]
