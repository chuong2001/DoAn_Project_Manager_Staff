from django.urls import path
from calendar_service import views

urlpatterns = [
    path("list_calender_by_part/<int:id_part>",views.list_calender_by_part,name="list_calender_by_part"),
    # path("update_post/<int:id_post>",views.update_post,name="update_post"),
    # path("all_post",views.all_post,name="all_post"),
    # path("delete_post/<int:id_post>",views.delete_post,name="delete_post"),
    # path('post_detail/<int:id_post>',views.post_detail,name="post_detail"),
]