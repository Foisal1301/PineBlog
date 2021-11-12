from django.shortcuts import get_object_or_404,redirect,render
from django.views import generic
from django.urls import reverse_lazy
from .forms import SignUpForm,EditProfileForm,PasswordChangingForm,CreateProfileForm
from django.contrib.auth.views import PasswordChangeView
from blog.models import Profile,Post,Category
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages

def delete_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user == request.user:
            logout(request)
            user.delete()
            messages.success(request, "User is deleted successfully!")
            return redirect('home')
        else:
            messages.success(request,"There was an error,try again!")
            return redirect('show-profile',args=request.user.id)
    else:
        return render(request,'registration/delete_user.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "User is deleted successfully!")
            return redirect('home')
        else:
            messages.success(request,"There was an error,try again!")
            return redirect('login_user',)
    else:
        return render(request,'registration/login.html',{})

#class DeleteUserView(generic.DeleteView):
#    model = User
#    template_name = "registration/delete_user.html"
#    success_url = reverse_lazy('home')

class CreateProfilePageView(generic.CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'registration/create_profile_page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateProfilePageView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = Category.objects.all()
        return context

class EditProfilePageView(generic.UpdateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'registration/edit_profile_page.html'
    #fields = ['bio','profile_pic','website_url','fb_url','twitter_url','insta_url','pinterest_url']

    def get_context_data(self, *args, **kwargs):
        context = super(EditProfilePageView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = Category.objects.all()
        return context

class ShowProfilePage(generic.DetailView):
    model = Profile
    template_name = "registration/profile.html"

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePage,self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile,id=self.kwargs['pk'])
        posts = Post.objects.filter(author=page_user.user)
        context['page_user'] = page_user
        context['posts'] = posts
        context['cat_menu'] = Category.objects.all()
        return context

class Password_ChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super(Password_ChangeView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = Category.objects.all()
        return context

#class SignUpView(generic.CreateView):
#    form_class = SignUpForm
#    template_name = 'registration/signup.html'
#    success_url = reverse_lazy('login')

def SignUpView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('create-profile')
    else:
        form = SignUpForm()

    return render(request,'registration/signup.html',{
        'form':form,
        'cat_menu':Category.objects.all()
    })

class PrivacySettingsView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/privacy_settings.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(PrivacySettingsView,self).get_context_data(*args, **kwargs)
        context['cat_menu'] = Category.objects.all()
        return context
