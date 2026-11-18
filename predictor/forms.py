from django import forms
from .models import StudentPerformance

class StudentPerformanceForm(forms.ModelForm):
    class Meta:
        model = StudentPerformance
        fields = ["student_name", "student_id", "attendance", "unit_tests", "assignments", "classwork"]
        widgets = {
            "student_name": forms.TextInput(attrs={"placeholder": "e.g. Samira Sharma"}),
            "student_id": forms.TextInput(attrs={"placeholder": "Optional student ID"}),
        }

    def clean(self):
        cleaned = super().clean()
        for field in ("attendance", "unit_tests", "assignments", "classwork"):
            value = cleaned.get(field)
            if value is not None and not 0 <= value <= 100:
                self.add_error(field, "Enter a value from 0 to 100.")
        return cleaned
