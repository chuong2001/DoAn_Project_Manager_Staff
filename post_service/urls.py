from django.urls import path
from post_service import views

urlpatterns = [
    path("add_post/<int:id_user>",views.add_post,name="add_post"),
    path("update_post/<int:id_post>",views.update_post,name="update_post"),
    path("all_post",views.all_post,name="all_post"),
    path("all_post_cmt",views.all_post_cmt,name="all_post_cmt"),
    path("all_type_post",views.all_type_post,name="all_type_post"),
    path("delete_post/<int:id_post>",views.delete_post,name="delete_post"),
    path('post_detail/<int:id_post>',views.post_detail,name="post_detail"),
    path("upload_image/<int:id_post>",views.upload_image,name="upload_image"),
]