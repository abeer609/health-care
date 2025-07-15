from django import forms
from django.conf import settings
from smart_parenting.models import Appointment, Doctor, Session
from unfold.widgets import UnfoldAdminTimeWidget


class UnfoldCustomAdminTimePicker(UnfoldAdminTimeWidget):
    template_name = "smart_parenting/widgets/time.html"

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format)

    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js",
            "smart_parenting/js/jquery.timepicker.min.js",
            "smart_parenting/js/time.js",
        ]
        css = {
            "all": [
                "smart_parenting/css/jquery.timepicker.min.css",
            ]
        }


class DoctorAdminForm(forms.ModelForm):
    visiting_hour_from = forms.TimeField(
        input_formats=["%I:%M %p"],
        widget=UnfoldCustomAdminTimePicker(format="%I:%M %p"),
    )
    visiting_hour_to = forms.TimeField(
        input_formats=["%I:%M %p"],
        widget=UnfoldCustomAdminTimePicker(format="%I:%M %p"),
    )

    def clean_visiting_hour_to(self):
        super().clean()
        if (
            self.cleaned_data["visiting_hour_to"]
            < self.cleaned_data["visiting_hour_from"]
        ):
            raise forms.ValidationError("Invalid time")
        return self.cleaned_data["visiting_hour_to"]

    class Meta:
        model = Doctor
        fields = "__all__"


class AppointmentAdminForm(forms.ModelForm):
    time = forms.TimeField(
        input_formats=["%I:%M %p"],
        widget=UnfoldCustomAdminTimePicker(format="%I:%M %p"),
    )

    class Meta:
        model = Appointment
        fields = "__all__"


class SessionAdminForm(forms.ModelForm):
    time = forms.TimeField(
        input_formats=["%I:%M %p"],
        widget=UnfoldCustomAdminTimePicker(format="%I:%M %p"),
    )

    class Meta:
        model = Session
        fields = "__all__"


class ChoicesWidget(forms.Select):
    template_name = "smart_parenting/widgets/select.html"

    def __init__(self, attrs=None, choices=()):
        if attrs is None:
            attrs = {"class": ""}
        attrs["class"] += " choices__autocomplete"
        super().__init__(attrs, choices)

    class Media:
        js = [
            "https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js",
            "smart_parenting/js/choices.init.js",
        ]
        css = {
            "all": [
                "https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css",
            ]
        }


class FlatpickrWidget(forms.DateInput):
    def __init__(self, attrs=None, format="Y-m-d"):
        if attrs is None:
            attrs = {}

        field_class = attrs.get("class")
        if field_class:
            attrs["class"] = attrs.get("class") + " flatpickr__datepicker"
        else:
            attrs["class"] = "flatpickr__datepicker"
        attrs["data-format"] = format
        super().__init__(attrs, format)

    class Media:
        js = [
            "https://cdn.jsdelivr.net/npm/flatpickr",
            "smart_parenting/js/flatpickr.init.js",
        ]
        css = {
            "all": [
                "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css",
            ]
        }


class TailwindForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            attrs = self.fields[field].widget.attrs
            field_class = attrs.get("class")
            if field_class is None:
                attrs["class"] = (
                    "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                )
            else:
                attrs["class"] = (
                    field_class
                    + " "
                    + "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                )


class AppointmentForm(TailwindForm):
    patient_name = forms.CharField(
        widget=forms.TextInput(attrs={"autocomplete": "off"})
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=ChoicesWidget(
            attrs={"data-placeholder": "Select Doctor", "class": "bg-gray-300"}
        ),
        initial="Select",
    )
    date = forms.DateField(widget=FlatpickrWidget(attrs={"placeholder": "Pick a date"}))
    time = forms.TimeField(
        widget=forms.Select(attrs={"data-placeholder": "Select Time"})
    )

    class Meta:
        model = Appointment
        fields = ["patient_name", "doctor", "date", "time"]
        exclude = ["user", "status"]
