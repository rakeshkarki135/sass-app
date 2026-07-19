

from django.urls import path

from apps.course.views import course_list, course_detail


urlpatterns = [
    path("", course_list, name="course_list"),
    path("<int:course_id>/", course_detail, name="course_detail"),
]
