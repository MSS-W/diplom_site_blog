from django.urls import path, re_path

from . import views

app_name = 'blog'
# Паттерны сайта
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.CategoryPageView.as_view(), name='category_page'),
    path('post/<slug:category_slug>/<slug:slug>/', views.PostPageView.as_view(), name='post_page'),
    path('search/', views.SearchPageView.as_view(), name='search_page'),
    re_path(r'^tag/(?P<tag_name>[\w-]+)/$', views.TagPageView.as_view(), name='tag_page'),
]
