from django.shortcuts import render
from .forms import StudentPerformanceForm
from .models import StudentPerformance
from .services import predict_score

def predict_grade(request):
    result = None
    if request.method == "POST":
        form = StudentPerformanceForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            score, grade, method = predict_score(
                student.attendance, student.unit_tests,
                student.assignments, student.classwork
            )
            student.predicted_score = score
            student.predicted_grade = grade
            student.save()
            result = {"student": student, "score": score, "grade": grade, "method": method}
            form = StudentPerformanceForm()
    else:
        form = StudentPerformanceForm()
    return render(request, "predictor/predict.html", {"form": form, "result": result})

def history(request):
    records = StudentPerformance.objects.all()[:100]
    return render(request, "predictor/history.html", {"records": records})
