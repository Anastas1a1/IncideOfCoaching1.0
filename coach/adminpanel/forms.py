from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateTimeInput

from .models import AdminProfile, File, FileTg, FileGoogle, UserProfile, Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['year', 'month']


class EditNameForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Имя пользователя'
        }

class NewUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tg_id': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Имя пользователя',
            'tg_id': 'Телеграм Id'
        }


class EditFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'

class EditFileTgForm(forms.ModelForm):
    class Meta:
        model = FileTg
        fields = '__all__'

class EditFileGoogleForm(forms.ModelForm):
    class Meta:
        model = FileGoogle
        fields = '__all__'

class EditSubscriptionsForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['year', 'month']
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.TextInput(attrs={'class': 'form-control'})
        }

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class EventForm(forms.ModelForm):
#     organizations = forms.ModelChoiceField(
#         queryset=Organization.objects.all(),
#         widget=forms.CheckboxSelectMultiple(),
#         label='Организации'
#     )

#     date = forms.DateTimeField(
#         widget=DateTimeInput(attrs={'type': 'datetime-local'}),
#         label='Дата и время'
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['organizations'].queryset = Organization.objects.all()
#         self.fields['organizations'].label_from_instance = lambda obj: obj.title

#     class Meta:
#         model = Event
#         fields = ['title', 'description', 'organizations', 'image', 'date']
#         labels = {
#             'title': 'Название мероприятия',
#             'description': 'Описание мероприятия',
#             'image': 'Изображение',
#             'date': 'Дата'
#         }

# class EventForm(forms.ModelForm):
#     organizations = forms.ModelMultipleChoiceField(
#         queryset=Organization.objects.all(),
#         widget=forms.Select(),
#         label='Организации'
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['organizations'].queryset = Organization.objects.all()
#         self.fields['organizations'].label_from_instance = lambda obj: obj.title

#     class Meta:
#         model = Event
#         fields = ['title', 'description', 'organizations', 'image', 'date']
#         labels = {
#             'title': 'Название мероприятия',
#             'description': 'Описание мероприятия',
#             'image': 'Изображение',
#             'date': 'Дата'
#         }
