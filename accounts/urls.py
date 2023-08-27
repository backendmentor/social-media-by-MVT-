from django.urls import path
from .import views
app_name="accounts"
urlpatterns = [
    path('register/', views.User_from_view.as_view(), name='register'),
    path('login/', views.LoginViewForm.as_view(), name='login'),
    path('logout/', views.logout_view_form.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.LoginProfile.as_view(), name='profile'),
    path('reset/', views.Reset_password_view.as_view(), name='password_reset'),
    path('reset/done/', views.Reset_password_view_done.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', views.Reset_password_view_confirm.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.Reset_password_view_complete.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.Following_view.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.Unfllowing_view.as_view(), name='unfollow'),
    path('editeprofile/', views.EditeUserView.as_view(), name='editporfile'),

]