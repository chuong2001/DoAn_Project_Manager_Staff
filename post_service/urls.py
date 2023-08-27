from django.urls import path
from post_service import views

urlpatterns = [
    path("add_post/<int:id_user>",views.add_post,name="add_post"),
    path("update_post/<int:id_post>",views.update_post,name="update_post"),
    path("all_post",views.all_post,name="all_post"),
    path("delete_post/<int:id_post>",views.delete_post,name="delete_post"),
    path('post_detail/<int:id_post>',views.post_detail,name="post_detail"),
]