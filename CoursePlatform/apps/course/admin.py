from django.contrib import admin
from apps.course.models import Course

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title","instructor","created_at","updated_at"]
    search_fields = ["title", "instructor__username"]
    list_filter = ["created_at", "updated_at", "instructor"]
