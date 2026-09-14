from django.shortcuts import render

from main.models import Experience
from main.models import Education
def show_main(request):
    context = {
        "name": "Isybal Sama Eleazar Malau",
        "npm" : "2506623963", "study_program" : "S1 Information System", 
        "bio": ("I love my team, I love my crew, urineun Seventeen inmida. Hey there I'm Ezar and I'm a third year Information System student at University of Indonesia with a passionate interest in making the world a much happier place. I'm passionate in graphic design as well as stuff in Kpop and everything music related. My favorite artists are Niki, Malcolm Todd, Seventeen, Aespa, and Olivia Rodrigo"),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name" : "Isybal Sama Eleazar Malau",
        "experience_list" : Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name" : "Isybal Sama Eleazar Malau",
        "education_list" : Education.objects.order_by(
            Case(
                When(end_year__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
            "-start_year",
            "institution",
        ),
    }
    return render(request, "education.html", context)
# Create your views here.
