from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from rest_framework import generics, filters, pagination
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

from django.shortcuts import redirect
from .forms import SubscriptionForm, EditNameForm, EditSubscriptionsForm
from .forms import EditFileForm, EditFileTgForm, EditFileGoogleForm, NewUserForm

from .models import AdminProfile, File, FileTg, FileGoogle, UserProfile, Subscription
from datetime import datetime
from django.http import JsonResponse


from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def users_list(request):
    user = request.user
    users_list = UserProfile.objects.all()
    files_list = File.objects.all()

    context = {
        'user': user,
        'users_list': users_list,
        'files_list': files_list
    }
    return render(request, 'users_list.html', context)


@login_required
def user_list(request):
    users_list = UserProfile.objects.all()
    return render(request, 'user_list.html', {'users_list': users_list})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    return redirect('user_list')

@login_required
def edit_username(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditNameForm(request.POST)
        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.save()
            return redirect('user_list')
    else:
        form = EditNameForm(initial={'name': user.name})

    context = {'form': form, 'user': user}
    return render(request, 'edit_username.html', context)

@login_required
def new_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        error_message = "Проверьте введённные данные и исправьте ошибки"
        form=NewUserForm()
    return render(request, 'new_user.html', {'form': form})



def user_subscriptions(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    subscriptions = Subscription.objects.filter(user=user)

    data = {
        'subscriptions': []
    }

    for subscription in subscriptions:
        data['subscriptions'].append({
            'subscription_date': subscription.subscription_date,
            'year': subscription.year,
            'month': subscription.month
        })

    return JsonResponse(data)


# def edit_subscriptions(request, user_id):
#     user = UserProfile.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = EditSubscriptionsForm(request.POST)
#         if form.is_valid():
#             return redirect('user_list')
#     else:
#         form = EditSubscriptionsForm()

#     context = {'form': form, 'user': user}
#     return render(request, 'edit_subscriptions.html', context)


@login_required
def user_profile(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    subscriptions = Subscription.objects.filter(user=user)

    context = {
        'user': user,
        'subscriptions': subscriptions
    }
    return render(request, 'user_profile.html', context)


@login_required
def edit_subscriptions(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    subscriptions = Subscription.objects.filter(user=user)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Обработка сохранения подписок
            # ...

            return redirect('user_profile', user_id=user_id)
    else:
        form = SubscriptionForm()

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'edit_subscriptions.html', context)


@login_required
def subscriptions_list(request):
    subs = Subscription.objects.all()
    return render(request, 'subscriptions_list.html', {'subs': subs})


@login_required
def file_list(request):
    file_list = File.objects.all()
    return render(request, 'file_list.html', {'file_list': file_list})





@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.delete()
    return redirect('file_list')



@login_required
def edit_file(request, file_id):
    file_obj = File.objects.get(id=file_id)
    
    try:
        file_tg_obj = FileTg.objects.get(file=file_obj)
        initial_tg = {'tg_id': file_tg_obj.tg_id, 'ext': file_tg_obj.ext}
    except FileTg.DoesNotExist:
        file_tg_obj = None
        initial_tg = {'tg_id': None, 'ext': None}
    
    try:
        file_google_obj = FileGoogle.objects.get(file=file_obj)
        initial_google = {'google_id': file_google_obj.google_id, 'link': file_google_obj.link}
    except FileGoogle.DoesNotExist:
        file_google_obj = None
        initial_google = {'google_id': None, 'link': None}

    if request.method == 'POST':
        file_form = EditFileForm(request.POST, instance=file_obj)
        file_tg_form = EditFileTgForm(request.POST, instance=file_tg_obj, initial=initial_tg)
        file_google_form = EditFileGoogleForm(request.POST, instance=file_google_obj, initial=initial_google)

        if file_form.is_valid() and file_tg_form.is_valid() and file_google_form.is_valid():
            file_form.save()
            if file_tg_form.cleaned_data['tg_id']:
                file_tg_form.save()
            if file_google_form.cleaned_data['google_id']:
                file_google_form.save()
            return redirect('file_list')
    else:
        file_form = EditFileForm(instance=file_obj)
        file_tg_form = EditFileTgForm(instance=file_tg_obj, initial=initial_tg)
        file_google_form = EditFileGoogleForm(instance=file_google_obj, initial=initial_google)

    context = {
        'file_form': file_form,
        'file_tg_form': file_tg_form,
        'file_google_form': file_google_form,
        'file_id': file_id,
    }
    print(context)
    return render(request, 'edit_file.html', context)




def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'logout.html')


@login_required
def home(request):
    user = request.user
    users_list = UserProfile.objects.all()
    files_list = File.objects.all()

    context = {
        'user': user,
        'users_list': users_list,
        'files_list': files_list
    }
    return render(request, 'home.html', context)
