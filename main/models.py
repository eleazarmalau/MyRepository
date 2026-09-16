import uuid

from django.db import models
from django.utils import timezone

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.CharField(max_length=500,blank=True, null=True)
    started_at = models.DateTimeField(default = timezone.now)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def organization(self):
        return self.place

    @property
    def is_ongoing(self):
        return self.ended_at is None or self.ended_at>timezone.now()


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length = 255)
    major = models.CharField(max_length = 255)
    description = models.TextField()
    thumbnail = models.CharField(max_length=500,blank=True, null=True)
    start_year = models.PositiveSmallIntegerField()
    end_year= models.PositiveSmallIntegerField(blank = True, null = True)

    class Meta:
        ordering = ["-start_year", "institution"]
        constraints = [models.CheckConstraint(
                        condition=(models.Q(end_year__isnull = True) 
                                   | models.Q(end_year__gte = models.F("start_year")))
                                   , name = "education_end_year_gte_start"),
        ]
    def __str__(self):
        return self.institution
    @property
    def description_items(self):
        return [
            line.strip()
            for line in self.description.splitlines()
            if line.strip()
        ]

# class Projects(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)