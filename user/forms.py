from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import Bio, Skill, Project
from django import forms as d_forms
from allauth.account.forms import SignupForm

User = get_user_model()

class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_usernamae":_("This username has already been taken")
        }
    )
    
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = {"username","email","name","type","password1","password2"}

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        raise ValidationError(
            self.error_messages["duplicate_username"]
    )


class HyreSignupForm(SignupForm):
    type = d_forms.ChoiceField(choices=[("HR","Hr"),("DEV","Dev")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["username"].widget.attrs["autofocus"]

        def custom_signup(self, request, user):
            user.type = self.cleaned_data['type']
            user.save()


# class BioForm(d_forms):
#     class Meta:
#         model = Bio
#         fields = ['bio']

# class SkillForm(d_forms):
#     class Meta:
#         model = Skill
#         fields = ['skill_string']

# class ProjectForm(d_forms):
#     class Meta:
#         model = Project
#         fields = ['name','link','desc']