from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .form import CustomUserCreationForm, UserProfileForm
from .models import CustomUser, UserProfile
from django.db.models.signals import post_save


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

def edit_profile(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)
    form = UserProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk_test)
    return render(request, "Account/edit_profile.html",{'get_user': get_user, 'profile': profile , 'form': form})

