from django.db.models import Case, IntegerField, Value, When
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from main.forms import ProjectForm, EducationForm, ExperienceForm
from main.models import Experience
from main.models import Education
from main.models import Project

import datetime
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Isybal Sama Eleazar Malau",
        "npm" : "2506623963", "study_program" : "S1 Information System", 
        "bio": ("I love my team, I love my crew, urineun Seventeen inmida. Hey there I'm Ezar and I'm a third year Information System student at University of Indonesia with a passionate interest in making the world a much happier place. I'm passionate in graphic design as well as stuff in Kpop and everything music related. My favorite artists are Niki, Malcolm Todd, Seventeen, Aespa, and Olivia Rodrigo"),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name" : "Isybal Sama Eleazar Malau",
        "experience_list" : Experience.objects.all(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

def show_education(request):
    json_response = get_educations_json(request)
    title_query = request.GET.get("title", "").strip()
    educations = serializers.deserialize(
            "json",
            json_response.content.decode("utf-8"),
        )
    educations = [education.object for education in educations]
    for education in educations:
        education.star_count = education.starred_by.count()

        education.is_starred = (
            request.user.is_authenticated
            and education.starred_by.filter(
                pk=request.user.pk
            ).exists()
        )
    context = {
        "name" : "Isybal Sama Eleazar Malau",
        "education_list" : educations,
        "title_query": title_query,
        "is_editor": is_editor(request.user),
    }
    return render(request, "education.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "title_query": title_query,
        "form": ProjectForm(),
        "project_list": projects,
        "is_editor": is_editor(request.user),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/") 
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def update_project(request, project_id):
    if not (
        request.user.is_superuser
        or is_editor(request.user)
    ):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(
        request.POST if request.method == "POST" else None,
        instance=project,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
        "project": project,
        "is_edit": True,
    }

    return render(request, "projects_form.html", context)

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Manually build the JSON data so we can add the Star logic
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def update_education(request, education_id):
    if not (
        request.user.is_superuser
        or is_editor(request.user)
    ):
        raise PermissionDenied
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

@login_required(login_url="/login/")
@require_POST
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)
    education.delete()
    messages.success(request, "Pendidikan berhasil dihapus!")
    return redirect("main:show_education")

@login_required(login_url="main:login")
@require_POST
def toggle_education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

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

    educations_json = serializers.serialize("json", educations,fields=[
        "title",
        "institution",
        "major",
        "description",
        "thumbnail",
        "start_year",
        "end_year",
        "created_at",
        "updated_at",
    ],)
    return HttpResponse(educations_json, content_type="application/json")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editor").exists()
    )

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Project added successfully.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def get_experiences_json(request):
    experiences = Experience.objects.all()

    experiences_json = serializers.serialize(
        "json",
        experiences,
        fields=[
            "title",
            "place",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "created_at",
            "updated_at",
        ],
    )

    return HttpResponse(
        experiences_json,
        content_type="application/json",
    )

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def update_experience(request, experience_id):
    if not (
        request.user.is_superuser
        or is_editor(request.user)
    ):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = EducationForm(
        request.POST if request.method == "POST" else None,
        instance=experience,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Isybal Sama Eleazar Malau",
        "form": form,
        "experience": experience,
        "is_edit": True,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")
# Create your views here.
