from .views import SignUpView,PrivacySettingsView,Password_ChangeView,ShowProfilePage,EditProfilePageView,CreateProfilePageView,delete_user
from . import views
from django.urls import path
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',SignUpView,name='signup'),
    path('privacy_setting/',PrivacySettingsView.as_view(),name='privacy-settings'),
    #path('password/',auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'),)
    path('password/',Password_ChangeView.as_view(template_name='registration/change_password.html'),name='change-password'),
    path('<int:pk>/profile/',ShowProfilePage.as_view(),name="show-profile"),
    path('<int:pk>/edit_profile/',EditProfilePageView.as_view(),name="edit-profile"),
    #path('<int:pk>/delete_account/',DeleteUserView.as_view(),name="delete-user"),
    path('create_profile/',CreateProfilePageView.as_view(),name="create-profile"),
    path('delete_account/',delete_user,name="delete-account"),
    path("login_user/",views.login_user,name='login-user')
]
