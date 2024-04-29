from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from recommendations.choices import GENRES

GENRE_PREFERENCES = (
    ("like", "Like"),
    ("dislike", "Dislike"),
    ("block", "Block"),
    ("neutral", "No Preference"),
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class GenreForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_preferences = kwargs.pop("initial_preferences", {})
        super(GenreForm, self).__init__(*args, **kwargs)

        filtered_genres = [  # skip no prefernce
            genre for genre in GENRES if not genre[0] == ""
        ]
        for genre in filtered_genres:
            genre_value = genre[0]
            genre_label = genre[1]
            self.fields[genre_value] = forms.ChoiceField(
                choices=GENRE_PREFERENCES,
                label=genre_label,
                widget=forms.RadioSelect,
                required=False,
                initial=initial_preferences.get(genre_value, "neutral"),
            )

    def clean(self):
        cleaned_data = super(GenreForm, self).clean()
        all_block = True
        all_dislike = True

        for genre_value, _ in GENRES:
            preference = cleaned_data.get(genre_value)

            if preference != "block":
                all_block = False

            if preference != "dislike":
                all_dislike = False

            if not all_block and not all_dislike:
                return cleaned_data

        if all_block or all_dislike:
            raise forms.ValidationError(
                "Not all genres can be set to 'Block' or 'Dislike'. Please choose a different preference for at least one genre."
            )


class CustomBooleanForm(forms.Form):
    """
    This form is used to collect user preferences for a users
    streaming services and triggers.
    """

    def __init__(self, *args, items=[], **kwargs):
        initial_preferences = kwargs.pop("initial_preferences", {})
        super(CustomBooleanForm, self).__init__(*args, **kwargs)

        filtered_items = [item for item in items if item[0] != ""]  # Skip no preference
        for item in filtered_items:
            item_value = item[0]
            item_label = item[1]
            self.fields[item_value] = forms.BooleanField(
                label=item_label,
                widget=forms.CheckboxInput,
                required=False,
                initial=initial_preferences.get(item_value, False),
            )
