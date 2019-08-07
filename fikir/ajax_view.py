from datetime import timedelta,datetime
from .models import * 
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,reverse

# Fikir beğenme AJAX
def likeAnIdea(request):
    ideaID = request.GET.get('ideaID', None)
    currentUser = request.user
    currentIdea = Idea.objects.get(pk=int(ideaID))
    if currentIdea.IsApproved and currentIdea.IsActive :
        currentUserProfile = UserProfile.objects.filter(UserT = currentUser).first()

        currentUserLike = UserLike.objects.filter(User=currentUserProfile).filter(Idea=currentIdea).first()
        if  currentUserLike:
            currentUserLike.delete()
        else:
            currentLike = UserLike()
            currentLike.Idea = currentIdea
            currentLike.User = currentUserProfile
            currentLike.LikeDate = datetime.now()
            currentLike.save() 
            
        currentcount = currentIdea.likes_list.all().count()
        data = {
            'likecount': currentcount,
            'status' : True
        }
        return JsonResponse(data)

    data = {
        'likecount': 0,
        'status' : False
    }
    return JsonResponse(data)


def load_neighborhood(request):
    district_id = request.GET.get('district')
    neigborhood_list = Neighborhood.objects.filter(District_id=district_id).order_by('Name')
    return render(request, 'partial/general/dropdown_list.html', {'object_list': neigborhood_list})

def load_street(request):
    neighborhood_id = request.GET.get('neighborhood')
    street_list = Street.objects.filter(Neighborhood_id=neighborhood_id).order_by('Name')
    return render(request, 'partial/general/dropdown_list.html', {'object_list': street_list})