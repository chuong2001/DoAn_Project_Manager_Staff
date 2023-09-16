from django.urls import path
from feedback_service import views

urlpatterns = [
    path("add_feedback/<int:id_user>",views.add_feedback,name="add_feedback"),
    # path("all_feedback",views.all_feedback,name="all_feedback"),
    path("delete_feedback/<int:id_feedback>",views.delete_feedback,name="delete_feedback"),
]