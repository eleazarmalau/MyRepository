from django.shortcuts import render

from main.models import Experience

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
# Create your views here.
