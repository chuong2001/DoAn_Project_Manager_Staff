from django.urls import path
from setting_service import views

urlpatterns = [
    path("update_setting",views.update_setting,name="update_setting"),
]