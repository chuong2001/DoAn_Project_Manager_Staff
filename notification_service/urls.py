from django.urls import path
from notification_service import views

urlpatterns = [
        path("get_all_notification/<int:id_user>",views.get_all_notification,name="get_all_notification"),
]