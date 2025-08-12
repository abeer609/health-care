import json
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
import datetime
from smart_parenting.forms import AppointmentForm, EmergencyForm
from smart_parenting.models import (
    AutismScreeningQuestion,
    Doctor,
    Response,
    Session,
    TeachingAid,
)
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
        return render(
            request, "smart_parenting/appointment.html", {"form": appointmentForm}
        )
    return render(
        request, "smart_parenting/appointment.html", {"form": appointmentForm}
    )


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
    form = EmergencyForm()
    if request.method == "POST":
        emergencyForm = EmergencyForm(request.POST)
        if emergencyForm.is_valid():
            emergency = emergencyForm.save(commit=False)
            emergency.user = request.user
            emergency.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Your emergency is successfully submitted. We will call you shortly!",
            )
        else:
            return render(
                request, "smart_parenting/EmergencyChild.html", {"form": emergencyForm}
            )
    return render(request, "smart_parenting/EmergencyChild.html", {"form": form})


def achievements(request):
    return render(request, "smart_parenting/achievementstories.html")


def ambulance(request):
    return render(request, "smart_parenting/ambulance.html")


def teaching_aids(request):
    teaching_aids = TeachingAid.objects.all()
    teaching_aid = TeachingAid.objects.first()
    active_url = teaching_aid.pk
    return render(
        request,
        "smart_parenting/teaching-aids.html",
        {
            "teaching_aids": teaching_aids,
            "teaching_aid": teaching_aid,
            "active_url": active_url,
        },
    )

def convert_to_boolean(string):
    return string.lower() == "true"

def teaching_aid(request, aid_id):
    teaching_aids = TeachingAid.objects.all()
    teaching_aid = TeachingAid.objects.get(id=aid_id)
    active_url = aid_id
    return render(
        request,
        "smart_parenting/teaching-aids.html",
        {
            "teaching_aids": teaching_aids,
            "teaching_aid": teaching_aid,
            "active_url": active_url,
        },
    )


def autism_screening_infants(request):
    questions = AutismScreeningQuestion.objects.filter(age="INFANTS")

    if request.method == "POST":
        request_body = json.loads(request.body)
        q_ids = []
        q_answers = []
        for resp in request_body:
            q_id = resp["question_id"]
            q_ans = resp["response"]
            q_ids.append(q_id)
            q_answers.append(q_ans)
        try:
            questions = AutismScreeningQuestion.objects.filter(pk__in=q_ids)
        except IntegrityError:
            return JsonResponse({"error": "Response already exists"}, status=400)
            # responses = Response.objects.all().select_related("question")
        score = 0
        for qs, ans in zip(questions, q_answers):
            if convert_to_boolean(ans)!= qs.expected_answer:
                score += 1
        print(score)
        if score <= 3:
            return JsonResponse({"risk": "LOW", "score": score})
        elif 3 < score <= 5:
            return JsonResponse({"risk": "MODERATE", "score": score})
        else:
            return JsonResponse({"risk": "HIGH", "score": score})
        
        
    return render(request, "smart_parenting/questions.html", {"questions": questions})


def autism_screening_toddlers(request):
    questions = AutismScreeningQuestion.objects.filter(age='TODDLERS')

    if request.method == "POST":
        request_body = json.loads(request.body)
        q_ids = []
        q_answers = []
        for resp in request_body:
            q_id = resp["question_id"]
            q_ans = resp["response"]
            q_ids.append(q_id)
            q_answers.append(q_ans)
        try:
            questions = AutismScreeningQuestion.objects.filter(pk__in=q_ids)
        except IntegrityError:
            return JsonResponse({"error": "Response already exists"}, status=400)
            # responses = Response.objects.all().select_related("question")
        score = 0
        for qs, ans in zip(questions, q_answers):
            if convert_to_boolean(ans)!= qs.expected_answer:
                score += 1
        if score <= 2:
            return JsonResponse({"risk": "LOW", "score": score})
        elif 2 < score <= 4:
            return JsonResponse({"risk": "MODERATE", "score": score})
        else:
            return JsonResponse({"risk": "HIGH", "score": score})
    return render(request, "smart_parenting/questions.html", {"questions": questions})


def autism_screening_preschoolers(request):
    questions = AutismScreeningQuestion.objects.filter(age='PRESCHOOLERS')

    if request.method == "POST":
        request_body = json.loads(request.body)
        q_ids = []
        q_answers = []
        for resp in request_body:
            q_id = resp["question_id"]
            q_ans = resp["response"]
            q_ids.append(q_id)
            q_answers.append(q_ans)
        try:
            questions = AutismScreeningQuestion.objects.filter(pk__in=q_ids)
        except IntegrityError:
            return JsonResponse({"error": "Response already exists"}, status=400)
            # responses = Response.objects.all().select_related("question")
        score = 0
        for qs, ans in zip(questions, q_answers):
            if convert_to_boolean(ans)!= qs.expected_answer:
                score += 1
        print(score)
        if score <= 3:
            return JsonResponse({"risk": "LOW", "score": score})
        elif 3 < score <= 5:
            return JsonResponse({"risk": "MODERATE", "score": score})
        else:
            return JsonResponse({"risk": "HIGH", "score": score})
    return render(request, "smart_parenting/questions.html", {"questions": questions})


def autism_screening_childrens(request):
    questions = AutismScreeningQuestion.objects.filter(age='CHILDREN')

    if request.method == "POST":
        request_body = json.loads(request.body)
        q_ids = []
        q_answers = []
        for resp in request_body:
            q_id = resp["question_id"]
            q_ans = resp["response"]
            q_ids.append(q_id)
            q_answers.append(q_ans)
        try:
            questions = AutismScreeningQuestion.objects.filter(pk__in=q_ids)
        except IntegrityError:
            return JsonResponse({"error": "Response already exists"}, status=400)
            # responses = Response.objects.all().select_related("question")
        score = 0
        for qs, ans in zip(questions, q_answers):
            if convert_to_boolean(ans)!= qs.expected_answer:
                score += 1
        print(score)
        if score <= 3:
            return JsonResponse({"risk": "LOW", "score": score})
        elif 3 < score <= 5:
            return JsonResponse({"risk": "MODERATE", "score": score})
        else:
            return JsonResponse({"risk": "HIGH", "score": score})
    return render(request, "smart_parenting/questions.html", {"questions": questions})