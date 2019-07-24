from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.contrib.auth import authenticate,login,logout
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
from django.core.paginator import Paginator
from enum import Enum
from django.http import JsonResponse

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
    ideas = Idea.objects.all().order_by('-id')[:3]
    # print(ideas[2].photo_set.first().Image.url)
    return render(request, template_name, {'object_list':ideas})

# Kullanıcı ana ekranı
def TimelineView(request):
    template_name = 'fikir/timeline.html'
    slideIdeas = Idea.objects.order_by('?').all().filter(IsOnHomePage=True)[:5]
    ideas_list = Idea.objects.all().filter(IsApproved=True).filter(IsActive=True)
    paginator = Paginator(ideas_list, 10) 
    page = request.GET.get('s')
    ideas = paginator.get_page(page)
    return render(request, template_name, {'ideas':ideas, 'slideIdeas':slideIdeas})


# Giriş sayfası
def DetailView(request):
    template_name = 'fikir/detail.html'
    return render(request, template_name)

# Profil sayfası
def ProfileView(request):
    template_name = 'fikir/profile.html'
    return render(request, template_name, {})

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
            newAddress = Address()
            newAddress.AdressDesc = form.cleaned_data['adressDesc']
            newAddress.District = form.cleaned_data['district']
            newAddress.Neighborhood = form.cleaned_data['neighborhood']
            newAddress.Street = form.cleaned_data['street']
            newAddress.save()

            # Yeni fikir oluşturma
            newIdea = Idea()
            newIdea.Title = form.cleaned_data['title']
            newIdea.Description = form.cleaned_data['description']
            newIdea.Ideatype = form.cleaned_data['ideatype']
            newIdea.Department = form.cleaned_data['department']
            newIdea.CreatedDate = datetime.datetime.now()
            newIdea.AddedUser = UserProfile.objects.filter(UserT = currentUser).first()
            newIdea.UserAddress = newAddress
            newIdea.IsApproved = False            
            newIdea.save()

            # Fikir fotoğrafları ekleme
            Photo1 = Photo()
            Photo2 = Photo()
            Photo3 = Photo()
            
            # Slider Photo
            Photo1.Image =  newAddress.AdressDesc = form.cleaned_data['ideaPhoto1']
            Photo1.ImageType = 1
            
            # Thumbnail
            Photo2.Image =  newAddress.AdressDesc = form.cleaned_data['ideaPhoto2']
            Photo2.ImageType = 2

            # Detail View
            Photo3.Image =  newAddress.AdressDesc = form.cleaned_data['ideaPhoto3']
            Photo3.ImageType = 3

            Photo1.Idea = newIdea
            Photo2.Idea = newIdea
            Photo3.Idea = newIdea

            Photo1.save()
            Photo2.save()
            Photo3.save()

            self.formVariables["messagetype"] = MessageType.success.name
            self.formVariables["messagetext"] = "Yeni fikriniz başarıyla oluşturuldu"
            return render(request,self.template_name,self.formVariables)

        # Başarısız form girdisi durumunda
        print(form.errors)
        self.formVariables["messagetype"] = MessageType.danger.name
        self.formVariables["messagetext"] = form.errors.values
        return render(request,self.template_name,self.formVariables)



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