from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from .forms import *
from django.views.generic.base import View
from django.contrib.auth.forms import *
from .models import *
from django.db.models import Prefetch
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from enum import Enum
from django.http import JsonResponse
from django.contrib import messages
from django.core.files.base import File
# Mesaj tipleri kullanım -> MessageType.danger.name
class MessageType(Enum):
    danger = 1
    warning = 2
    success = 3
    info = 4

# Giriş sayfası
def IndexView(request):
    template_name = 'fikir/homepage.html'
    # threeIdeas = Idea.objects.all().order_by('?')[0:3]
    ideas = Idea.objects.all().order_by('-id').filter(IsApproved=True).filter(IsActive=True)[:3]
    # print(ideas[2].photo_set.first().Image.url)
    return render(request, template_name, {'object_list':ideas})

# Kullanıcı ana ekranı
def TimelineView(request):
    template_name = 'fikir/timeline.html'
    slideIdeas = Idea.objects.order_by('?').all().filter(IsOnHomePage=True).filter(IsActive=True).filter(IsApproved=True)[:5]
    ideas_list = Idea.objects.all().filter(IsApproved=True).filter(IsActive=True)
    paginator = Paginator(ideas_list, 6) 
    page = request.GET.get('page')

    try:
        ideas = paginator.page(page)
    except PageNotAnInteger:
        ideas = paginator.page(1)
    except EmptyPage:
        ideas = paginator.page(paginator.num_pages)

    return render(request, template_name, {'ideas':ideas, 'slideIdeas':slideIdeas})


# Giriş sayfası
def DetailView(request, pk):
    template_name = 'fikir/detail.html'
    current_idea = Idea.objects.get(pk=pk)
    return render(request, template_name, {"current_idea":current_idea})

# Profil sayfası
def ProfileView(request):
    template_name = 'fikir/profile.html'
    currentUserProfile = UserProfile.objects.all().filter(UserT=request.user).first()
    
    # Fikirlerim
    myideas = Idea.objects.all().filter(IsActive=True).filter(IsApproved=True).filter(AddedUser__UserT=request.user)
    myideas_paginator = Paginator(myideas, 6) 
    myideas_page = request.GET.get('myideas_page')
    try:
        myideas = myideas_paginator.page(myideas_page)
    except PageNotAnInteger:
        myideas = myideas_paginator.page(1)
    except EmptyPage:
        myideas = myideas_paginator.page(myideas_paginator.num_pages)

    # Beğendiğim Fikirler
    mylikeideas = Idea.objects.all().filter(pk__in=currentUserProfile.userliked_list.values_list('Idea', flat=True))
    
    mylikeideas_paginator = Paginator(mylikeideas, 6) 
    mylikeideas_page = request.GET.get('mylikeideas_page')
    try:
        mylikeideas = mylikeideas_paginator.page(mylikeideas_page)
    except PageNotAnInteger:
        mylikeideas = mylikeideas_paginator.page(1)
    except EmptyPage:
        mylikeideas = mylikeideas_paginator.page(mylikeideas_paginator.num_pages)

    return render(request, template_name, {
        "myideas":myideas,
        "is_settings_menu_display":True,
        "mylikeideas":mylikeideas,
        'current_profile':currentUserProfile})

# Profil Ayarları sayfası
class ProfileSettingsView(View):
    form_class = UserEditForm
    template_name = "fikir/profilesettings.html"
    formVariables = {'form': form_class,
    'pagetitle':'Profil Güncelleme',
    'form_title':'Profilini Güncelle',
    'buttontext' : "Güncelle",
    'messagetext':'',
    'messagetype':''}
    def get(self, request):
        self.formVariables["messagetype"] = ""
        current_user_profile = UserProfile.objects.all().filter(UserT=request.user).first()
        self.formVariables["form"] = UserEditForm(instance=current_user_profile)
        self.formVariables["form_password"] = CustomPasswordChangeForm(user=request.user)
        self.formVariables["form_password_action"] = reverse('fikir:ChangePassword', kwargs={})
        self.formVariables["form_profile_action"] = reverse('fikir:ProfileSettings', kwargs={})
        self.formVariables["messagetext"] = ""
        return render(request, self.template_name, self.formVariables)
    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            current_user_profile= UserProfile.objects.filter(UserT = request.user).first()
            current_user_profile.Name = form.cleaned_data['Name']
            current_user_profile.Surname = form.cleaned_data['Surname']
            current_user_profile.PhoneNumber = form.cleaned_data['PhoneNumber']
            current_user_profile.Birthday = form.cleaned_data['Birthday']
            current_user_profile.Email = form.cleaned_data['Email']
            new_profile_photo = form.cleaned_data['ProfilePhoto']
            if new_profile_photo is not None :
                current_user_profile.ProfilePhoto = form.cleaned_data['ProfilePhoto']
            current_user_profile.save()
            self.formVariables["messagetype"] = MessageType.success.name
            self.formVariables["messagetext"] = "Profil başarıyla güncellendi"
            self.formVariables["form"] = UserEditForm(instance=current_user_profile)
            return render(request, self.template_name, self.formVariables)


        self.formVariables["messagetype"] = MessageType.danger.name
        self.formVariables["messagetext"] = form.errors.values
        return render(request, self.template_name, self.formVariables)

# Giriş ekranı
class LoginView(View):
    form_class = LoginForm
    template_name = "fikir/login.html"
    formVariables = {
    'form': form_class,
    'pagetitle':'Giriş',
    'formtitle':'Giriş',
    'buttontext' : 'Giriş',
    'messagetext':'',
    'messagetype':''}
    def get(self, request):
        self.formVariables["messagetype"] = ""
        self.formVariables["messagetext"] = ""
        return render(request, self.template_name, self.formVariables)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if not form.cleaned_data.get('remember_me'):
                        request.session.set_expiry(0)
                    login(request, user)
                    return redirect('fikir:TimelineView')
            self.formVariables["messagetype"] = MessageType.warning.name
            self.formVariables["messagetext"] = "Kullanıcı Adı veya Parola Yanlış"
            return render(request, self.template_name, self.formVariables)
        
        self.formVariables["messagetext"] = "Değerler geçersiz"
        self.formVariables["messagetype"] = MessageType.warning.name
        return render(request, self.template_name, self.formVariables)

# Üye olma
class UserFormView(View):
    form_class = UserForm
    template_name = "fikir/signup.html"
    formVariables = {'form': form_class(None),
    'pagetitle':'Üye Ol',
    'formtitle':'Fikirlerini Paylaşmak İçin Üye Ol',
    'buttontext' : "Üye Ol",
    'messagetext':'',
    'messagetype':''}
    def get(self, request):
            return render(request, self.template_name,self.formVariables)

    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # Kullanici oluşturma
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # Kullanıcıya bağlı kullanıcı profili oluşturma
            userprofile = UserProfile()
            userEmail = form.cleaned_data['email']

            userprofile.Name            = form.cleaned_data['name']
            userprofile.Surname         = form.cleaned_data['surname']
            userprofile.PhoneNumber     = form.cleaned_data['phoneNumber']
            userprofile.Birthday        = form.cleaned_data['birthday']
            userprofile.Email           = userEmail
            userprofile.ProfilePhoto    = form.cleaned_data['profilePhoto']
            userprofile.District      = form.cleaned_data['district']
            userprofile.UserT           = user
            userprofile.save()

            # Aktivasyon maili gönderme
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your blog account.'
            # message = render_to_string('active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activation_token.make_token(user),
            # })
            # to_email = userEmail
            # email = EmailMessage(
            #             mail_subject, message, to=[to_email]
            # )
            # email.send()
            # Oluşturulan Kullanıcıyla giriş yapma
            user = authenticate(username = username,password= password)
            if  user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('fikir:IndexView')

        self.formVariables["messagetype"] = MessageType.danger.name
        self.formVariables["messagetext"] = form.errors.values
        return render(request,self.template_name,self.formVariables)



# Listelemeler

def Timeline(request):
    ideas_list = Idea.objects.all().filter(IsApproved=True).filter(IsActive=True)
    paginator = Paginator(ideas_list, 10) 
    page = request.GET.get('page')
    ideas = paginator.get_page(page)






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
            currentLike.LikeDate = datetime.datetime.now()
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

# Parola Değiştirme
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        old_password = form.cleaned_data['old_password']
        new_password1 = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('fikir:ProfileSettings')
    else:
        messages.error(request, 'Please correct the error below.')
    return redirect('fikir:ProfileSettings')

# Fikir güncelleme
class UpdateIdeaView(View):
    template_name = "fikir/addingform.html"
    formVariables = {
    'form': "",
    'pagetitle':'Fikir Güncelle',
    'formtitle':'Fikir Güncelleme',
    'buttontext' : 'Güncelle',
    'messagetext':'',
    'messagetype':''}
    def get(self, request, pk):
        current_idea = Idea.objects.filter(id=pk).filter(AddedUser__UserT_id=request.user.id).first()
        if current_idea is not None:
            self.formVariables["form"] = UpdateIdeaForm(instance=current_idea)
            self.formVariables["messagetype"] = ""
            self.formVariables["messagetext"] = ""
            return render(request, self.template_name, self.formVariables)
        redirect("fikir:ProfileView")

    def post(self, request, pk):
        form = UpdateIdeaForm(request.POST,request.FILES)
        self.formVariables["pk"] = pk
        if form.is_valid():
            current_idea = Idea.objects.get(pk=pk)
            current_idea.Title       = form.cleaned_data['Title']
            current_idea.Description = form.cleaned_data['Description']
            current_idea.Ideatype    = form.cleaned_data['Ideatype']
            current_idea.Department  = form.cleaned_data['Department']
            current_idea.AdressDesc  = form.cleaned_data['AdressDesc']
            current_idea.District    = form.cleaned_data['District']
            current_idea.Neighborhood= form.cleaned_data['Neighborhood']
            current_idea.Street      = form.cleaned_data['Street']

            # Idea Photo Kontrol

            new_idea_photo = form.cleaned_data['ideaPhoto']
            if new_idea_photo is not None :
                Photo.objects.filter(Idea=current_idea).delete()

                # Fikir fotoğrafları güncelleme
                new_idea_photo = File(form['ideaPhoto'].value())

                # Slider Photo
                CurrentPhoto1 = Photo()
                CurrentPhoto1.Idea = current_idea
                CurrentPhoto1.Image = new_idea_photo
                CurrentPhoto1.ImageType = 1
                CurrentPhoto1.save()
                
                # Thumbnail
                CurrentPhoto2 = Photo()
                CurrentPhoto2.Idea = current_idea
                CurrentPhoto2.Image = new_idea_photo
                CurrentPhoto2.ImageType = 2
                CurrentPhoto2.save()

                # Detail View
                CurrentPhoto3 = Photo()
                CurrentPhoto3.Idea = current_idea
                CurrentPhoto3.Image = new_idea_photo
                CurrentPhoto3.ImageType = 3
                CurrentPhoto3.save()


            current_idea.save()
            self.formVariables["form"] = UpdateIdeaForm(instance=current_idea)
            self.formVariables["messagetype"] = MessageType.success.name
            self.formVariables["messagetext"] = "Fikir başarıyla güncellendi"
            return render(request,self.template_name,self.formVariables)
        
        
        self.formVariables["messagetype"] = MessageType.danger.name
        self.formVariables["messagetext"] = form.errors.values
        return render(request,self.template_name,self.formVariables)

# Yeni fikir ekleme
class NewIdeaView(View):
    form_class = NewIdeaForm
    template_name = "fikir/addingform.html"
    formVariables = {
    'form': form_class,
    'pagetitle':'Yeni Fikir',
    'formtitle':'Yeni Fikir',
    'buttontext' : 'Ekle',
    'messagetext':'',
    'messagetype':''}
    def get(self, request):
        self.formVariables["messagetype"] = ""
        self.formVariables["messagetext"] = ""
        return render(request, self.template_name, self.formVariables)

    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            # Giriş yapan kullanıcıyı alma
            currentUser = request.user
            # Yeni Adres oluşturma

            # Yeni fikir oluşturma
            newIdea = Idea()
            newIdea.Title       = form.cleaned_data['Title']
            newIdea.Description = form.cleaned_data['Description']
            newIdea.Ideatype    = form.cleaned_data['Ideatype']
            newIdea.Department  = form.cleaned_data['Department']
            newIdea.CreatedDate = datetime.datetime.now()
            newIdea.AddedUser   = UserProfile.objects.filter(UserT = currentUser).first()
            newIdea.AdressDesc  = form.cleaned_data['AdressDesc']
            newIdea.District    = form.cleaned_data['District']
            newIdea.Neighborhood= form.cleaned_data['Neighborhood']
            newIdea.Street      = form.cleaned_data['Street']
            newIdea.IsApproved = False            
            newIdea.save()

            # Fikir fotoğrafları ekleme
            IdeaPhoto = File(form['ideaPhoto'].value())

            # Slider Photo
            CurrentPhoto1 = Photo()
            CurrentPhoto1.Idea = newIdea
            CurrentPhoto1.Image = IdeaPhoto
            CurrentPhoto1.ImageType = 1
            CurrentPhoto1.save()
            
            # Thumbnail
            CurrentPhoto2 = Photo()
            CurrentPhoto2.Idea = newIdea
            CurrentPhoto2.Image = IdeaPhoto
            CurrentPhoto2.ImageType = 2
            CurrentPhoto2.save()

            # Detail View
            CurrentPhoto3 = Photo()
            CurrentPhoto3.Idea = newIdea
            CurrentPhoto3.Image = IdeaPhoto
            CurrentPhoto3.ImageType = 3
            CurrentPhoto3.save()

            self.formVariables["messagetype"] = MessageType.success.name
            self.formVariables["messagetext"] = "Yeni fikriniz başarıyla oluşturuldu"
            return render(request,self.template_name,self.formVariables)

        # Başarısız form girdisi durumunda
        print(form.errors)
        self.formVariables["messagetype"] = MessageType.danger.name
        self.formVariables["messagetext"] = form.errors.values
        return render(request,self.template_name,self.formVariables)



# Üyelik Aktive Etme
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('fikir:IndexView')
    else:
        return HttpResponse('Aktivasyon maili geçersiz')