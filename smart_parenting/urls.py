from django.urls import path

from . import views

app_name = "smart_parenting"

urlpatterns = [
    path("", views.index, name="index"),
    path("appointment/", views.appointment, name="appointment"),
    path("sessions/", views.sessions, name="sessions"),
    path("teaching-aids/", views.teaching_aids, name="teaching_aids"),
    path("screening/infants/", views.autism_screening_infants, name="infants_screening"),
    path("screening/toddlers/", views.autism_screening_toddlers, name="toodlers_screening"),
    path("screening/preschoolers/", views.autism_screening_preschoolers, name="toodlers_screening"),
    path("screening/childrens/", views.autism_screening_childrens, name="toodlers_screening"),
    path("teaching-aids/<int:aid_id>/", views.teaching_aid, name="teaching_aid"),
    path("available/", views.get_doctor_available_time),
    path("doctors/", views.doctor),
    path("emergency/", views.emergency, name='emergency'),
    path("achievements/", views.achievements),
    path("ambulance/", views.ambulance),
    path("child-care/", views.child_care),
    path("calendar/", views.calendar),
]
