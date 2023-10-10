from django.urls import path
from user_service import views

urlpatterns = [
    path("register_user",views.register_user,name="register_user"),
    path("update_user/<int:id_user>",views.update_user,name="update_user"),
    path("login",views.login,name="login"),
    path("all_user",views.all_user,name="all_user"),
    path("update_part/<int:id_user>/<int:id_part>",views.update_part,name="update_part"),
    path("update_position/<int:id_user>/<int:id_position>",views.update_part,name="update_part"),
    path("all_part",views.all_part,name="all_part"),
    path("all_position_by_part/<int:id_part>",views.all_position_by_part,name="all_position_by_part"),
    path("get_admin",views.get_admin,name="get_admin"),
    path("get_part/<int:id_part>",views.get_part,name="get_part"),
    path("delete_user/<int:id_user>",views.delete_user,name="delete_user"),
    path('user_detail/<int:id_user>',views.user_detail,name="user_detail"),
    path('change_password/<int:id_user>',views.change_password,name="change_password"),
]