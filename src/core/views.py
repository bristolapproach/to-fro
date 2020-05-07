from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from actions.views import ActionsListView
from django.contrib.auth.views import LoginView
from tofro.lib import has_permission


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def homepage(request):
    if (has_permission(request.user)):
        return ActionsListView.as_view(list_type='mine')(request)
    else:
        return LoginView.as_view()(request)
