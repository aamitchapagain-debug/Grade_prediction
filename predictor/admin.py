from django.contrib import admin
from .models import StudentPerformance

@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_id", "attendance", "unit_tests",
                    "assignments", "classwork", "predicted_score", "predicted_grade", "created_at")
    search_fields = ("student_name", "student_id")
    list_filter = ("predicted_grade", "created_at")
