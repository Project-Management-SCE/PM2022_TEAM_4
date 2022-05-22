from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .form import CustomUserCreationForm, UserProfileForm, RequestForm, MessageForm, CommentForm, SupportTicketForm,\
    RequestChangeForm, CommentChangeForm
from .models import CustomUser, UserProfile, RequestModel, MessageModel, CommentModel
from django.db.models.signals import post_save
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from operator import attrgetter


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
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists():
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

@login_required()
def edit_request(request,pk_test,pk):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        posts = RequestModel.objects.get(id=pk)
        form = RequestChangeForm(request.POST or None, instance=posts)
        if request.method == 'POST':
            form = RequestChangeForm(request.POST, request.FILES, instance=posts)
            if form.is_valid():
                form.save()
                messages.success(request,'Your request has been changed successfully!')
                return redirect('user_profile', pk_test)
        return render(request, "Account/edit_request.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

@login_required()
def edit_comment(request,pk_test,pk):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        comments = CommentModel.objects.get(id=pk)
        form = CommentChangeForm(request.POST or None, instance=comments)
        if request.method == 'POST':
            form = CommentChangeForm(request.POST, request.FILES, instance=comments)
            if form.is_valid():
                form.save()
                messages.success(request,'Your comments has been changed successfully!')
                pk=comments.user.id
                return redirect('view_request', pk_test,pk)
        return render(request, "Account/edit_comment.html",{'get_user': get_user, 'profile': profile , 'form': form})
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
#change 1
@login_required()
def close_request(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        user_request = RequestModel.objects.get(pk=pk)
        user_request.close = True
        user_request.save()
        messages.success(request, 'The request closed successfully!')
        return redirect('user_profile', pk_test)
    else:
        messages.success(request, 'You can not close another users request!')
        return render(request, 'home/HomePage.html')

@login_required()
def messaging(request,pk_test):
    if request.user.username != pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=request.user.username)
        get_receiver = CustomUser.objects.get(username=pk_test)
        profilerec = UserProfile.objects.get(user=get_receiver)
        profile = UserProfile.objects.get(user=get_user)
        Historysender = MessageModel.objects.filter(sender=request.user,receiver=get_receiver).order_by('created_at')
        Historyreciver = MessageModel.objects.filter(sender=get_receiver, receiver=request.user).order_by('created_at')
        History = sorted(chain(Historysender, Historyreciver), key=attrgetter('created_at'))
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.sender = request.user
                instance.receiver = CustomUser.objects.get(username=pk_test)
                #instance.receiver = CustomUser.objects.get(username=form.cleaned_data['receiver'])
                instance.save()
                messages.success(request,'Your message has been sent successfully! to- '+ profilerec.first_name)
                return redirect('messaging', pk_test)
        else:
            form = MessageForm()
        return render(request, "Account/messaging.html",{'get_user': get_user, 'profile': profile , 'form': form,'get_receiver':get_receiver,'History':History})
    else:
        messages.success(request, 'You do not have permission to send a message to a user that is not you!')
        return render(request, 'home/HomePage.html')


# Display the messages that the user received
@login_required()
def inbox(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
        return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})
    else:
        messages.success(request, 'You do not have permission to view this inbox!')
        return render(request, 'home/HomePage.html')

@login_required()
def messaging_read(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        messagess = MessageModel.objects.get(id=pk)
        messagess.read =True
        messagess.save()
        messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
        messages.success(request, 'You inbox is update successfully!')
        return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})

@login_required()
def messaging_delete(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='Support').exists():
            get_user = CustomUser.objects.get(username=pk_test)
            profile = UserProfile.objects.get(user=get_user)
            messagess = MessageModel.objects.get(id=pk)
            MessageModel.delete(messagess)
            messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
    return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})

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

@user_passes_test(lambda u: u.is_superuser,login_url='home')
def delete_user(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)
    CustomUser.delete(get_user)
    UserProfile.delete(profile)
    messages.success(request, 'You Delete user successfully!')
    return render(request, 'home/HomePage.html')

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def delete_request(request,pk_test,pk):
    user_request = RequestModel.objects.get(pk=pk)
    RequestModel.delete(user_request)
    messages.success(request, 'You Delete Request successfully!')
    return render(request, 'home/HomePage.html')


@login_required()
def support_ticket(request):
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    # check if user is in support group
    if request.method == 'POST' and request.user.groups.filter(name='support').exists():
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,'Your support ticket has been sent successfully!')
            return render(request, 'home/HomePage.html')
    else:
        form = SupportTicketForm()
    return render(request, "Account/support_ticket.html",{'get_user': get_user, 'profile': profile , 'form': form})



# Admin function to display amount of users
@user_passes_test(lambda u: u.is_superuser,login_url='home')
def user_count(request):
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    users = CustomUser.objects.all()
    user_c = users.count()
    return render(request, "Account/user_count.html",{'get_user': get_user, 'profile': profile , 'user_c': user_c})




