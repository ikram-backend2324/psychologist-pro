from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import AGE_GROUPS, SPOKEN_LANGUAGES, User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        label=_("I am joining as"),
        choices=[(User.Role.CLIENT, _("Client")), (User.Role.PSYCHOLOGIST, _("Psychologist"))],
        widget=forms.RadioSelect,
        initial=User.Role.CLIENT,
    )
    first_name = forms.CharField(label=_("First name"), max_length=150)
    last_name = forms.CharField(label=_("Last name"), max_length=150, required=False)
    email = forms.EmailField(label=_("Email"), required=False)
    specialization = forms.CharField(
        label=_("Specialization"),
        max_length=150,
        required=False,
        help_text=_("For psychologists, e.g. “Family psychology”."),
    )
    age_group = forms.ChoiceField(
        label=_("Your age group"),
        choices=[("", _("Prefer not to say"))] + AGE_GROUPS,
        required=False,
        help_text=_("Helps us suggest psychologists who work with your age."),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("role", "first_name", "last_name", "username", "email", "specialization", "age_group")

    def clean(self):
        data = super().clean()
        if data.get("role") == User.Role.PSYCHOLOGIST and not data.get("specialization"):
            self.add_error("specialization", _("Please tell clients what you specialize in."))
        return data


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class CommaMultipleChoiceField(forms.MultipleChoiceField):
    """Stores a list of choices in a comma-separated CharField."""

    widget = forms.CheckboxSelectMultiple

    def prepare_value(self, value):
        if isinstance(value, str):
            return [v for v in value.split(",") if v]
        return value

    def clean(self, value):
        return ",".join(super().clean(value))


class ProfileForm(forms.ModelForm):
    age_groups = CommaMultipleChoiceField(label=_("I work with"), choices=AGE_GROUPS, required=False)
    spoken_languages = CommaMultipleChoiceField(label=_("Consultation languages"), choices=SPOKEN_LANGUAGES, required=False)

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "age_group",
            "specialization", "experience_years", "age_groups", "spoken_languages", "accepts_clients", "bio",
        )
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "email": _("Email"),
            "specialization": _("Specialization"),
            "experience_years": _("Years of experience"),
            "bio": _("About me"),
            "age_group": _("Your age group"),
            "accepts_clients": _("I accept new clients"),
        }
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.is_psychologist:
            self.fields.pop("age_group")
        else:
            for name in ("specialization", "experience_years", "age_groups", "spoken_languages", "accepts_clients", "bio"):
                self.fields.pop(name)
