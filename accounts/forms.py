from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from recommendations.choices import GENRES

PREFERENCES = (
    ("like", "Like"),
    ("dislike", "Dislike"),
    ("block", "Block"),
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class GenreForm(forms.Form):
    """
    This form is used to collect user preferences for each genre,
    the genre choices come from recommendations.choices.GENRES
    """

    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        for genre in GENRES:
            genre_value = genre[0]
            genre_label = genre[1]
            self.fields[genre_value] = forms.ChoiceField(
                choices=PREFERENCES,
                label=genre_label,
                widget=forms.RadioSelect,
                required=False,
            )
