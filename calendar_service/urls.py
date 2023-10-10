from django.urls import path
from calendar_service import views

urlpatterns = [
    path("list_calender_by_part/<int:id_part>",views.list_calender_by_part,name="list_calender_by_part"),
    path("add_calendar/<int:id_part>/<int:id_type_calendar>",views.add_calendar,name="add_calendar"),
    path("update_calendar/<int:id_calendar>/<int:id_part>/<int:id_type_calendar>",views.update_calendar,name="update_calendar"),
    path("all_type_calendar",views.all_type_calendar,name="all_type_calendar"),
    path("delete_calendar/<int:id_calendar>",views.delete_calendar,name="delete_calendar"),
    path('get_calendar/<int:id_calendar>',views.get_calendar,name="get_calendar"),
]