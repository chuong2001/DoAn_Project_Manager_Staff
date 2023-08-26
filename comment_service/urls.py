from django.urls import path
from comment_service import views

urlpatterns = [
    path("add_comment/<int:id_user>/<int:id_post>",views.add_comment,name="add_comment"),
    path("update_comment/<int:id_comment>",views.update_comment,name="update_comment"),
    path("all_comment/<int:id_post>",views.all_comment,name="all_comment"),
    path("delete_comment/<int:id_comment>",views.delete_comment,name="delete_comment"),
    path('comment_detail/<int:id_comment>',views.comment_detail,name="comment_detail"),
]