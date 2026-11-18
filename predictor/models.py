from django.db import models

class StudentPerformance(models.Model):
    student_name = models.CharField(max_length=120)
    student_id = models.CharField(max_length=40, blank=True)
    attendance = models.FloatField(help_text="Attendance percentage (0–100)")
    unit_tests = models.FloatField(help_text="Average unit-test score (0–100)")
    assignments = models.FloatField(help_text="Average assignment score (0–100)")
    classwork = models.FloatField(help_text="Average classwork score (0–100)")
    predicted_score = models.FloatField(null=True, blank=True)
    predicted_grade = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student_name} — {self.predicted_grade or 'Not predicted'}"
