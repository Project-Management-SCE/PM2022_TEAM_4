from django.shortcuts import render
import folium
from geopy import distance
from Account.models import UserProfile,CustomUser
from django.core.paginator import Paginator

def home(request):
    get_user = CustomUser.objects.all()
    profile = UserProfile.objects.all()
    #set up pagination
    p = Paginator(get_user,5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request,'home/HomePage.html',{'page_obj':page_obj,'profile':profile})

def map(request):
    #get who is login to system
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    #add to map who is login
    m = folium.Map(location=[profile.latitude,profile.longitude],zoom_start=15)
    print(profile.image.url)
    userIcon = 'http://127.0.0.1:8000' + profile.image.url
    icon = folium.features.CustomIcon(userIcon, icon_size=(28, 30))
    folium.Marker([profile.latitude, profile.longitude], tooltip="You here!", popup="<a href=https://http://127.0.0.1:8000>Help Me</a>",icon=icon).add_to(m)
    #make the raduis circle
    folium.Circle(location=[profile.latitude, profile.longitude], radius=100).add_to(m)
    #save Lat and lan who login
    newport_ri = (profile.latitude, profile.longitude)
    all_user = CustomUser.objects.all()
    #check all user who is distunation 0.1 km
    for user in all_user:
        tempProfile = UserProfile.objects.get(user=user)
        if tempProfile:
            cleveland_oh = (tempProfile.latitude, tempProfile.longitude)
            #get the lan and lat from all user and add to map if under 0.1
            if distance.distance(newport_ri, cleveland_oh).km <= 0.1 and tempProfile != profile:
                otherusericon='http://127.0.0.1:8000' + tempProfile.image.url
                icon = folium.features.CustomIcon(otherusericon, icon_size=(28, 30))
                folium.Marker([tempProfile.latitude, tempProfile.longitude], tooltip="click for help me "+user.username, popup='אני צריך מקדחה' ,icon=icon).add_to(m)
    m = m._repr_html_()
    context = { 'm':m,'profile':profile}
    return render(request,'home/Map.html',context)
