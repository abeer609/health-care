from django.urls import path

from . import views

app_name = "smart_parenting"
urlpatterns = [
    path("", views.index, name="index"),
    path("appointment/", views.appointment, name="appointment"),
    path("sessions/", views.sessions, name="sessions"),
    path("available/", views.get_doctor_available_time),
    path("doctors/", views.doctor),
    path("emergency/", views.emergency),
    path("achievements/", views.achievements),
    path("ambulance/", views.ambulance),
    path("child-care/", views.child_care),
    path("calendar/", views.calendar),
]
