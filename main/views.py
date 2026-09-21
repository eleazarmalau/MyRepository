from django.db.models import Case, IntegerField, Value, When
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from main.forms import ProjectForm, EducationForm
from main.models import Experience
from main.models import Education
from main.models import Project
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
    json_response = get_educations_json(request)
    
    educations = serializers.deserialize(
            "json",
            json_response.content.decode("utf-8"),
        )
    educations = [education.object for education in educations]
    title_query = request.GET.get("title", "").strip()
    context = {
        "name" : "Isybal Sama Eleazar Malau",
        "education_list" : educations,
        "title_query": title_query,
    }
    return render(request, "education.html", context)

...
def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Jenjang Edukasi baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
    }
    return render(request, "educations_form.html", context)

@require_http_methods(["GET", "POST"])
def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(
        request.POST if request.method == "POST" else None,
        instance=education,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
        "education": education,
        "is_edit": True,
    }
    return render(request, "educations_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def get_educations_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.order_by(
        Case(
            When(end_year__isnull=True, then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        ),
        "-start_year",
        "institution",
    )

    if title_query:
        educations = educations.filter(title__icontains=title_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")
# Create your views here.
