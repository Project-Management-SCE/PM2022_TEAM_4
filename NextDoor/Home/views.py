from django.shortcuts import render
import folium
from geopy import distance
from Account.models import UserProfile,CustomUser,MessageModel
from django.core.paginator import Paginator

def home(request):
    if request.user.is_authenticated:
        messages = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
        mes=0
        for m in messages:
            if m.read==False:
                mes=mes+1
        get_user = CustomUser.objects.all().order_by('?')
        profile = UserProfile.objects.all()
        #set up pagination
        p = Paginator(get_user,6)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        return render(request,'home/HomePage.html',{'page_obj':page_obj,'profile':profile,'mes':mes})
    else:
        get_user = CustomUser.objects.all().order_by('?')
        profile = UserProfile.objects.all()
        p = Paginator(get_user,6)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        return render(request,'home/HomePage.html',{'page_obj':page_obj,'profile':profile})


def map(request):
    #get who is login to system
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    #add to map who is login
    m = folium.Map(location=[profile.latitude,profile.longitude],zoom_start=15)
    m.get_root().html.add_child(folium.Element("""
    <style>
    .leaflet-container .leaflet-overlay-pane svg, .leaflet-container .leaflet-marker-pane img, .leaflet-container .leaflet-shadow-pane img, .leaflet-container .leaflet-tile-pane img, .leaflet-container img.leaflet-image-layer, .leaflet-container .leaflet-tile {
    max-width: none !important;
    max-height: none !important;
    border-radius: 20px;
}
    </style>
    """
    ))
    m.save("Map.html")
    print(profile.image.url)
    userIcon = 'http://127.0.0.1:8000' + profile.image.url
    icon = folium.features.CustomIcon(userIcon, icon_size=(28, 30))
    popup_string = "<a href=http://127.0.0.1:8000/Account/user_profile/" + get_user.username + "/requests target =_blank rel=noopener noreferrer>My Requests</a>"
    folium.Marker([profile.latitude, profile.longitude], tooltip="You are here!", popup=popup_string,icon=icon).add_to(m)
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
                # Folium Marker: tooltip = user.username, popup is a link to the user's profile
                popup_string = "<a href=http://127.0.0.1:8000/Account/user_profile/" + user.username + "/requests target =_blank rel=noopener noreferrer>Help Me</a>"
                folium.Marker([tempProfile.latitude, tempProfile.longitude], tooltip=user.username,
                              popup=popup_string,icon=icon).add_to(m)
                # popup redirection
                # folium.Marker([tempProfile.latitude, tempProfile.longitude], tooltip=user.username,
                #               popup=popup_string,icon=icon).add_to(m)


    m = m._repr_html_()
    context = { 'm':m,'profile':profile}
    return render(request,'home/Map.html',context)


def search(request):
    users = CustomUser.objects.all()
    profile = UserProfile.objects.all()
    context = {}
    list = []
    if request.method == 'POST':
        name = request.POST.get('s')
        print(name)
        for u in users:
            if name in u.username:
                list.append(u)
    context = {'users': users, 'name': name, 'list': list, 'profile': profile}
    return render(request, 'home/search.html', context)
