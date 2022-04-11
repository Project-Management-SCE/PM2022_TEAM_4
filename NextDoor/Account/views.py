from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .form import CustomUserCreationForm, UserProfileForm
from .models import CustomUser, UserProfile
from django.db.models.signals import post_save
from django.contrib.auth import authenticate
from django.contrib import messages

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Account/signup.html'
    def post(self, request, *args, **kwargs):
        pass
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })



def user_profile(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)

    return render(request, "Account/user_profile.html",{'get_user': get_user, 'profile': profile})


@login_required()
def edit_profile(request,pk_test):
    if request.user.username==pk_test:
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        form = UserProfileForm(request.POST or None, instance=profile)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request,'Your Profile has been changed successfully!')
                return redirect('user_profile', pk_test)
        return render(request, "Account/edit_profile.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

