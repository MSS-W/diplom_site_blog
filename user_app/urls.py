from django.urls import path
from django.contrib.auth import views as auth_views

from user_app import views

app_name = 'user_app'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.CustomUserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user_app/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user_app/password_reset_done.html'),
         name='password_reset_done'),
    path('<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('<str:username>/settings/', views.UserSettingsView.as_view(), name='user_profile_settings'),
    path('<str:username>/posts/', views.UserPostsView.as_view(), name='user_posts'),
    path('post/add_post/', views.AddPostByAuthorView.as_view(), name='add_post'),
    path('post/add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('post/add_file/', views.AddFileView.as_view(), name='add_file'),
    path('post/edit_post/<int:pk>', views.EditPostByAuthorView.as_view(), name='edit_post'),
    path('post/delete_post/<int:pk>', views.DeletePostByAuthorView.as_view(), name='delete_post'),
]
