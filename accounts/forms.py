from django import forms
# forms: from django import forms
from .models import Profile
from django.contrib.auth.models import User
# Django already provides a built-in User model. Instead of creating our own user table, we use Django's existing User model.

class RegisterForm(forms.ModelForm):
    # There are 2 types of forms. 1)Form:we define every field manually 2)ModelForm: Django automatically creates form fields from a database model. 
     password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        }),
        min_length=6
    )

     username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'off'
        })
    )

     email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off'
        })
    )

    # A widget controls: How the field appears in HTML, by using passwordInput: when user enters the password it will be hidden ,shows like: *****

     class Meta:
        # Meta provides configuration/settings for the form
        model=User #Build this form using User model
 
        # user model actually has many fields in it, here Django tells to include the following fields only.
        fields=[
            'username',
            'email',
            'password'
        ]
     def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'bio',
            'profile_pic'
        ]