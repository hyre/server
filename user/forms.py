from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import Bio, Skill, Project
from django import forms as d_forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

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


class AuthForm(AuthenticationForm):
    username = d_forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Email', 'id':'exampleInputEmail1'}))
    password = d_forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password', 'id':'exampleInputPassword1'}))




class BioForm(d_forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['bio','user', 'age', 'city', 'country']

class SkillForm(d_forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_string','user']
   

class ProjectForm(d_forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','link','desc','user']
    