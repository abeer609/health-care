from datetime import datetime
from django.contrib import admin
from django.db import models
from .models import Appointment, Doctor, Response, Session, TeachingAid, Emergency, AutismScreeningQuestion
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.widgets import UnfoldAdminFileFieldWidget
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
from .forms import AppointmentAdminForm, DoctorAdminForm, SessionAdminForm


@admin.register(Doctor)
class DoctorAdmin(UnfoldModelAdmin):
    list_display = [
        "name",
        "specialization",
        "visiting_hour_from",
        "visiting_hour_to",
        "weekend",
    ]
    search_fields = ["name", "email"]
    form = DoctorAdminForm


@admin.register(Session)
class SessionAdmin(UnfoldModelAdmin):
    list_display = ["title", "date", "time", "session_link"]
    search_fields = ["title"]
    autocomplete_fields = ["users"]
    form = SessionAdminForm

    def get_changeform_initial_data(self, request):
        items = request.GET.items()
        data = {}
        for k, v in items:
            if k == "time":
                dt = datetime.strptime(v, "%H:%M:%S")
                data[k] = dt.strftime("%I:%M %p")
            else:
                data[k] = v
        return data


@admin.register(Appointment)
class AppointmentAdmin(UnfoldModelAdmin):
    list_display = [
        "patient_name",
        "date",
        "time",
        "doctor__name",
        "appointment_status",
        "user",
        "action",
    ]
    search_fields = ['patient_name']
    list_filter = ['status']
    autocomplete_fields = ["doctor", "user"]
    form = AppointmentAdminForm

    @admin.display(description="Status", ordering="status")
    def appointment_status(self, obj):
        STATUS_CLASS_MAP = {
            "pending": "text-amber-600",
            "approved": "text-green-700",
            "completed": "text-blue-500",
        }
        STATUS_ICON_MAP = {
            "pending": "<span class='material-symbols-outlined'> schedule </span>",
            "approved": "<span class='material-symbols-outlined'> verified </span>",
            "completed": "<span class='material-symbols-outlined'>check_circle</span>",
        }
        return mark_safe(
            f"<div class='flex items-center gap-1 {STATUS_CLASS_MAP[obj.status]}'>{STATUS_ICON_MAP[obj.status]}<p>{str.capitalize(obj.status)}</p></div>"
        )

    def action(self, obj):
        params = urlencode(
            {
                "date": obj.date,
                "title": f"Session for {obj.patient_name}",
                "users": obj.user.id,
                "appointment": obj.id,
                "time": obj.time,
            }
        )
        if obj.status == "pending":
            return mark_safe(
                f"<div><a class='bg-primary-600 text-xs w-min border border-transparent cursor-pointer font-medium px-3 py-1 rounded-default text-white' href='/admin/smart_parenting/session/add/?{params}'>Approve</a></div>"
            )
        else:
            return ""


@admin.register(TeachingAid)
class TeachingAidAdmin(UnfoldModelAdmin):
    list_display = ["title", "uploaded_at"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.FileField) and db_field.name == "video":
            kwargs["widget"] = UnfoldAdminFileFieldWidget(attrs={"accept": "video/*"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# print(UnfoldAdminField(DoctorForm, "email", is_first=False))

@admin.register(Emergency)
class EmergencyAdmin(UnfoldModelAdmin):
    list_display = ['full_name']

@admin.register(AutismScreeningQuestion)
class AutismScreeningQuestionAdmin(UnfoldModelAdmin):
    list_display = ['title', 'age', 'expected_answer']
    list_editable = ['age', 'expected_answer']
    list_filter = ['age']

@admin.register(Response)
class AutismScreeningQuestionAdmin(UnfoldModelAdmin):
    list_display = ['user__username', 'answer']
