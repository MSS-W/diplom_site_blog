from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import PostModel, CategoryModel, PostFilesModel
from user_app import forms
from user_app.decorators import set_template
from user_app.mixins import (
    PermissionSameAuthorMixin,
    PermissionGroupRequiredMixin
)

class CustomLoginView(LoginView):
    authentication_form = forms.LoginForm
    template_name = 'user_app/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def get_success_url(self):
        return reverse_lazy('blog:index')


class CustomRegistrationView(CreateView):
    form_class = forms.RegistrationForm
    template_name = 'user_app/signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy('user_app:login')

    def form_valid(self, form):
        form.save()
        group = Group.objects.get(name='Пользователь')
        form.instance.groups.add(group)
        form.instance.save()
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_app/password_reset.html'
    email_template_name = 'user_app/password_reset_email.html'
    form_class = forms.CustomPasswordResetForm
    success_url = reverse_lazy('user_app:password_reset_done')


class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_app/password_reset_confirm.html'
    success_url = reverse_lazy('user_app:password_reset_complete')
    form_class = forms.CustomSetPasswordForm


class UserProfileView(TemplateView):  
    template_name = 'user_app/profile_page.html'  
    author_template_name = 'user_app/profile_page_author.html'  
    is_author = False  
    extended_group = 'Автор'  
  
    @set_template(author_template_name, 'is_author')  
    def dispatch(self, request, *args, **kwargs):  
        return super().dispatch(request, *args, **kwargs)  
  
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        try:  
            user = get_object_or_404(User, username=self.kwargs.get('username'))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        context['user_profile'] = user  
        context['is_author'] = self.is_author  
        if self.is_author:  
            context['drafts'] = PostModel.objects.filter(author=user, status='ЧЕ')[:7]  
        context['user_posts'] = PostModel.post_manager.filter(author=user)[:7]  
        context['title'] = f'Профиль пользователя {user}'  
        return context


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/profile_settings_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info_form'] = forms.UserInfoForm(instance=self.request.user)
        context['user_profile_form'] = forms.ProfileForm(instance=self.request.user.profile)
        context['user_password_form'] = forms.UserPasswordForm(self.request.user)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context

    def post(self, request, *args, **kwargs):
        if 'user_info_form' in request.POST:
            user_info_form = forms.UserInfoForm(request.POST, instance=request.user)
            user_profile_form = forms.ProfileForm(request.POST, request.FILES, instance=self.request.user.profile)
            if user_info_form.is_valid() and user_profile_form.is_valid():
                user_info_form.save()
                user_profile_form.save()
                messages.success(request, 'Данные успешно изменены.')
                return redirect('user_app:user_profile_settings', user_info_form.cleaned_data.get('username'))
            else:
                context = self.get_context_data(**kwargs)
                context['user_info_form'] = user_info_form
                context['user_profile_form'] = user_profile_form
                return render(request, self.template_name, context)
        elif 'user_password_form' in request.POST:
            form = forms.UserPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменён.')
                return self.get(request, *args, **kwargs)
            else:
                context = self.get_context_data(**kwargs)
                context['user_password_form'] = form
                return render(request, self.template_name, context)
        else:
            return self.get(request, *args, **kwargs)


class UserPostsView(ListView):
    template_name = 'user_app/user_posts_page.html'
    author_template_name = 'user_app/user_posts_page_author.html'
    context_object_name = 'posts'
    paginate_by = 10
    is_author = False
    extended_group = 'Автор'

    @set_template(author_template_name, 'is_author')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.is_author:
            return (PostModel.objects.filter(author__username=self.kwargs.get('username'))
                    .order_by('-status', '-publish'))
        else:
            return PostModel.post_manager.filter(author__username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            author = get_object_or_404(User, username=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['author'] = author
        context['title'] = f'Посты пользователя {author}'
        context['is_author'] = self.is_author
        return context


class PostByAuthor:
    template_name = 'user_app/add_post.html'
    group_required = 'Автор'
    form_class = forms.AddPostByAuthorForm
    model = PostModel

    def get_success_url(self):
        return reverse('user_app:user_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)[:50]
        form.instance.author = self.request.user
        return super().form_valid(form)
       
        
class AddPostByAuthorView(PostByAuthor, PermissionGroupRequiredMixin, CreateView):
    extra_context = {'title': 'Добавление поста'}


class EditPostByAuthorView(PostByAuthor, PermissionSameAuthorMixin, UpdateView):
    extra_context = {'title': 'Изменить пост'}


class DeletePostByAuthorView(PermissionSameAuthorMixin, DeleteView):
    template_name = 'user_app/delete_post_confirm.html'
    model = PostModel
    group_required = 'Автор'
    extra_context = {'title': 'Удалить пост?'}

    def get_success_url(self):
        return reverse_lazy('user_app:user_profile', kwargs={'username': self.request.user.username})


class AddCategoryAndFile(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.groups.filter(name='Автор').exists()

    def get_success_url(self):
        return reverse('user_app:user_profile', kwargs={'username': self.request.user.username})


class AddCategoryView(AddCategoryAndFile):
    template_name = 'user_app/add_category.html'
    form_class = forms.AddCategoryByAuthorForm
    model = CategoryModel
    extra_context = {'title': 'Добавление категории'}

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class AddFileView(AddCategoryAndFile):
    template_name = 'user_app/add_file.html'
    form_class = forms.AddFileByAuthorForm
    model = PostFilesModel
    extra_context = {'title': 'Добавление файла'}
    
