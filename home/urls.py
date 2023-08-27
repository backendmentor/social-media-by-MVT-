from django.urls import path
from .import views

app_name="home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/<int:id_post>/<str:slug_post>/', views.PostView.as_view(), name='post_detail'),
    path('posts/delete/<int:post_id>/', views.Postdelete.as_view(), name='delete_detail'),
    path('posts/update/<int:id_post>/', views.view_update.as_view(), name='update_detail'),
    path('posts/create/', views.Creatview_post_comment.as_view(), name='create_detail'),
    path('reply/<int:post_id>/<int:comment_id>/', views.ReplyView.as_view(), name='add_reply'),
    path('like/<int:post_id>/', views.LikeView.as_view(), name='like_view'),



]