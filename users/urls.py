from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.AjaxLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('profile/password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('profile/password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/password_reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/password_reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

