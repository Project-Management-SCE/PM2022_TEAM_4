from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .form import CustomUserCreationForm, UserProfileForm, RequestForm, MessageForm, CommentForm
from .models import CustomUser, UserProfile, RequestModel, MessageModel, CommentModel
from django.db.models.signals import post_save
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings



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
    posts = RequestModel.objects.filter(user=get_user).order_by('created_at')
    if posts:
        last_request = posts.last().created_at
    else:
        last_request = None

    return render(request, "Account/user_profile.html",{'get_user': get_user, 'profile': profile, 'posts':posts, 'last_request':last_request})


@login_required()
def edit_profile(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        form = UserProfileForm(request.POST or None, instance=profile)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                address = request.POST.get('location', False)
                city = request.POST.get('locality', False)
                country = request.POST.get('country', False)
                apt = request.POST.get('apt', False)
                lat = request.POST.get('lat', False)
                lng = request.POST.get('lng', False)
                instance = form.save(commit=False)
                instance.address = address
                instance.city = city
                instance.country = country
                instance.postal_code = apt
                instance.latitude = lat
                instance.longitude = lng
                form.save()
                messages.success(request,'Your Profile has been changed successfully!')
                return redirect('user_profile', pk_test)
        return render(request, "Account/edit_profile.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

def Rulse(request):
    return render(request, 'Account/Rulse.html')


# Allow the user to create a request
@login_required()
def create_request(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        if request.method == 'POST':
            form = RequestForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request,'Your request has been sent successfully!')
                return redirect('user_profile', pk_test)
        else:
            form = RequestForm()
        return render(request, "Account/create_request.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to create a request!')
        return render(request, 'home/HomePage.html')

# Display the requests that the user has made
@login_required()
def requests(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)
    requests = RequestModel.objects.filter(user=get_user).order_by('created_at')
    return render(request, "Account/requests.html",{'get_user': get_user, 'profile': profile , 'requests': requests})


@login_required()
def messaging(request,pk_test):
    if request.user.username != pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=request.user.username)
        get_receiver = CustomUser.objects.get(username=pk_test)
        #get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.sender = request.user
                instance.receiver = CustomUser.objects.get(username=pk_test)
                #instance.receiver = CustomUser.objects.get(username=form.cleaned_data['receiver'])
                instance.save()
                messages.success(request,'Your message has been sent successfully!')
                return redirect('user_profile', pk_test)
        else:
            form = MessageForm()
        return render(request, "Account/messaging.html",{'get_user': get_user, 'profile': profile , 'form': form,'get_receiver':get_receiver})
    else:
        messages.success(request, 'You do not have permission to send a message to a user that is not you!')
        return render(request, 'home/HomePage.html')


# Display the messages that the user received
@login_required()
def inbox(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
        return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})
    else:
        messages.success(request, 'You do not have permission to view this inbox!')
        return render(request, 'home/HomePage.html')



@login_required()
def view_request(request,pk_test,pk):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)
    user_request = RequestModel.objects.get(pk=pk)
    comments = CommentModel.objects.filter(request=user_request).order_by('created_at')
    # Allow a user to comment on a request
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.request = user_request
            instance.save()
            messages.success(request,'Your comment has been sent successfully!')
            return redirect('view_request', pk_test,pk)
    else:
        form = CommentForm()

    return render(request, "Account/view_request.html",{'get_user': get_user, 'profile': profile , 'user_request': user_request, 'comments': comments, 'form': form})



