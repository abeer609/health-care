import datetime
from django.db import models
from user.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class WeekendsChoice(models.IntegerChoices):
    SUNDAY = 0, "Sunday"
    MONDAY = 1, "Monday"
    TUESDAY = 2, "Tuesday"
    WEDNESDAY = 3, "Wednesday"
    THURSDAY = 4, "Thursday"
    FRIDAY = 5, "Friday"
    SATURDAY = 6, "Saturday"


# def visiting_hour_validator(value):


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    duration = models.PositiveIntegerField(
        verbose_name="Duration (in minutes)", default=60
    )
    visiting_hour_from = models.TimeField()
    visiting_hour_to = models.TimeField()
    weekend = models.IntegerField(choices=WeekendsChoice, default=WeekendsChoice.FRIDAY)

    def __str__(self):
        return self.name


class Session(models.Model):
    title = models.CharField(max_length=250)
    appointment = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    session_link = models.URLField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    users = models.ManyToManyField(User, blank=True)
    open_for_all = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        dt = datetime.datetime.combine(self.date, self.time)
        if datetime.datetime.now() < dt:
            return True
        return False

    def __str__(self):
        return self.title


# class SessionPermission(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     users = models.ManyToManyField(User)
#     open_for_all = models.BooleanField(default=False)


class AppointmentStatus(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    patient_name = models.CharField(max_length=250)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=AppointmentStatus, default=AppointmentStatus.PENDING
    )

    def __str__(self):
        return f"Appointment #{self.id}"

    class Meta:
        unique_together = [["doctor", "date", "time"]]


# class UserSession(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


# class Counsel(models.Model):


class TeachingAid(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    video = models.FileField(
        upload_to="teaching-aids",
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mkv", "mov"])],
        blank=True,
        null=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Emergency(models.Model):
    full_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    details = models.TextField()
    live_location = models.JSONField(null=True, blank=True)
    file = models.FileField(upload_to='emergencies', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=Session)
def update_appointment_status(sender, instance, created, **kwargs):
    if created and instance.session_link:
        appointment = instance.appointment
        appointment.status = "approved"
        appointment.save()

class AutismScreeningQuestion(models.Model):
    YES_NO_CHOICES = [
            (True, "Yes"),
            (False, "No"),
        ]
    
    class ChildrenAgeRange(models.TextChoices):
        INFANTS = "INFANTS", "Infants (6-12 months)"
        TODDLERS = "TODDLERS", "Toddlers (12-24 months)"
        PRESCHOOLERS = "PRESCHOOLERS", "Preschoolers (2-5 years)"
        CHILDREN = "CHILDREN", "Children (6-12 years)"

    class QuestionType(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    title = models.TextField()
    age = models.CharField(max_length=20, choices=ChildrenAgeRange, default=ChildrenAgeRange.INFANTS)
    expected_answer = models.BooleanField(choices=YES_NO_CHOICES, default=True)
    question_importance = models.CharField(max_length=10, choices=QuestionType, default=QuestionType.LOW)
    # is_low_weight = models.BooleanField(default=False)

class Response(models.Model):
    YES_NO_CHOICES = [
        (True, "Yes"),
        (False, "No"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(AutismScreeningQuestion, on_delete=models.CASCADE, related_name="responses")
    answer = models.BooleanField(choices=YES_NO_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question")  # Prevents duplicate answers

