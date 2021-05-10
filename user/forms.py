from django import forms

from user.models import User, Profile


class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'sex', 'birth_day', 'location']


class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
