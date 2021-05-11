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

    def clean_max_dating_age(self):
        '''检查最大交友年龄'''
        cleaned = super().clean()
        if cleaned['min_dating_age'] > cleaned['max_dating_age']:
            raise forms.ValidationError('min_dating_age 大于 max_dating_age')
        else:
            return cleaned['max_dating_age']

    def clean_max_distance(self):
        '''检查最大交友距离'''
        cleaned = super().clean()
        if cleaned['min_distance'] > cleaned['max_distance']:
            raise forms.ValidationError('min_distance 大于 max_distance')
        else:
            return cleaned['max_distance']
