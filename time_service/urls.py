from django.urls import path
from time_service import views

urlpatterns = [
    path("add_time/<int:id_user>",views.add_time,name="add_time"),
    path("get_time_user/<int:id_user>",views.get_time_user,name="get_time_user"),
    path("get_time_all",views.get_time_all,name="get_time_all"),
]