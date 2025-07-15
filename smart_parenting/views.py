import json
from django.http import JsonResponse
from django.shortcuts import render
import datetime
from smart_parenting.forms import AppointmentForm
from smart_parenting.models import Doctor, Session
from django.db.models import Q
from django.conf import settings


def index(request):
    return render(request, "smart_parenting/index.html")


def appointment(request):
    appointmentForm = AppointmentForm()
    if request.method == "POST":
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.user = request.user
            appointment.save()
    return render(request, "smart_parenting/counseling.html", {"form": appointmentForm})


def generate_timeslots(
    start, end, interval=settings.SESSION_DURATION, date=datetime.date.today()
):
    start = datetime.datetime.combine(date, start)
    end = datetime.datetime.combine(date, end)
    dt = datetime.timedelta(minutes=interval)
    times = []
    while start < end:
        time = start.time()
        if start + dt <= end:
            times.append(time)
        start += dt
    return times


def get_doctor_available_time(request):
    if request.method == "POST":
        body = json.loads(request.body)
        doctor = Doctor.objects.get(pk=body["doctor_id"])
        date = body["date"]
        visiting_hour_from = doctor.visiting_hour_from
        visiting_hour_to = doctor.visiting_hour_to
        duration = doctor.duration
        appointments = doctor.appointment_set.filter(date=date).values_list(
            "time", flat=True
        )
        # sessions = Session.objects.filter(
        #     appointment_id__in=appointments, date=date
        # ).values_list("time", flat=True)

        time_slots = generate_timeslots(
            visiting_hour_from, visiting_hour_to, interval=duration
        )
        response = []
        for time in time_slots:
            if time not in appointments:
                dt = datetime.datetime.combine(datetime.datetime.today(), time)
                to = dt + datetime.timedelta(minutes=duration)
                response.append(
                    {
                        "value": dt.time().strftime("%H:%M"),
                        "label": f"{dt.time().strftime("%I:%M %p")} - {to.time().strftime("%I:%M %p")}",
                    }
                )

        # response = [
        #     {
        #         "value": time.strftime("%H:%M"),
        #         "label": f"{time.strftime("%I:%M %p")} - {time+datetime.timedelta(minutes=duration)}",
        #     }
        #     for time in time_slots
        #     if time not in appointments
        # ]

        return JsonResponse({"slots": response})


def sessions(request):
    user = request.user
    query = Q(users__pk=user.id) | Q(open_for_all=True)
    sessions = Session.objects.select_related("appointment").filter(query)
    return render(request, "smart_parenting/session.html", {"sessions": sessions})


def child_care(request):
    return render(request, "smart_parenting/childcare.html")


def calendar(request):
    return render(request, "smart_parenting/calendar.html")


def doctor(request):
    return render(request, "smart_parenting/doctor.html")


def emergency(request):
    return render(request, "smart_parenting/EmergencyChild.html")


def achievements(request):
    return render(request, "smart_parenting/achievementstories.html")


def ambulance(request):
    return render(request, "smart_parenting/ambulance.html")
