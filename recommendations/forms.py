from django import forms

from .choices import *


class GenreForm(forms.Form):
    Question = forms.CharField(
        initial="Let's pick your desired genre(s)!", disabled=True, max_length=50
    )

    OPTIONS = GENRES
    Genres = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=OPTIONS
    )

    FILTERS = [
        ("And", "Movies Contain All Selected Genres"),
        ("Or", "Movies Contain at Least One Selected Genre"),
    ]
    Filters = forms.ChoiceField(
        widget=forms.RadioSelect, choices=FILTERS, initial=FILTERS[0]
    )


class YearForm(forms.Form):
    Question = forms.CharField(
        initial="What release time frame are you feeling today?",
        disabled=True,
        max_length=50,
    )

    OPTIONS = YEAR_SPANS
    Years = forms.ChoiceField(
        widget=forms.RadioSelect, choices=OPTIONS, initial=OPTIONS[0], required=False
    )


class RuntimeForm(forms.Form):
    Question = forms.CharField(
        initial="And what time duration?",
        disabled=True,
        max_length=50,
    )

    OPTIONS = RUNTIME_SPANS
    Runtimes = forms.ChoiceField(
        widget=forms.RadioSelect, choices=OPTIONS, initial=OPTIONS[0], required=False
    )


class LanguageForm(forms.Form):
    Question = forms.CharField(
        initial="Pick some languages! Pick at least three.",
        disabled=True,
        max_length=50,
    )

    OPTIONS = LANGUAGES
    Languages = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=OPTIONS
    )


class TriggerForm(forms.Form):
    Question = forms.CharField(
        initial="Do you have any triggers?",
        disabled=True,
        max_length=50,
    )

    OPTIONS = TRIGGERS
    Triggers = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=OPTIONS, initial=OPTIONS[0]
    )
