from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput

from main.models import Project, Education

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

# id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)
#     institution = models.CharField(max_length = 255)
#     major = models.CharField(max_length = 255)
#     description = models.TextField()
#     thumbnail = models.CharField(max_length=500,blank=True, null=True)
#     start_year = models.PositiveSmallIntegerField()
#     end_year=
class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "title",
            "institution",
            "major",
            "description",
            "thumbnail",
            "start_year",
            "end_year",
        ]

        labels = {
            "title": "Jenjang Edukasi",
            "institution": "Nama Institusi",
            "major": "Nama Jurusan",
            "description": "Deskripsi Singkat Kegiatan Edukasi",
            "thumbnail" : "URL Gambar Institusi",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "S1 Sistem Informasi",
                    "maxlength": 255,
                }
            ),
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                    }
            ),
            "major": TextInput(
                attrs={
                    "placeholder": "Sistem Informasi",
                    "maxlength": 255,
                    }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan kegiatan selama pendidikan",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "Kosongkan jika masih berlangsung",
                }
            ),
        }

def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get("start_year")
        end_year = cleaned_data.get("end_year")

        if start_year is not None and end_year is not None and end_year < start_year:
            self.add_error("end_year", "Tahun selesai tidak boleh sebelum tahun mulai.")

        return cleaned_data