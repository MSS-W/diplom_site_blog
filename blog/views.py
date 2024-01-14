from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from blog import models, forms


class IndexView(TemplateView):
    """ Представление главной страницы """
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        """
        Переопределённый метод get_context_data().
        Передаёт в шаблон дополнительные данные.
        """
        context = super().get_context_data(**kwargs)
        context['categories_list'] = models.CategoryModel.objects.all()
        context['latest_posts'] = models.PostModel.post_manager.latest_posts()
        context['popular_posts'] = models.PostModel.post_manager.popular_posts()
        return context


class CategoryPageView(ListView):
    """ Представление страницы категории """
    model = models.PostModel
    template_name = 'blog/category_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """
        Переопределённый метод get_queryset().
        Возвращает все посты категории, включая посты в подкатегориях.
        """
        category = self.get_category()
        descendant_categories = category.get_descendants(include_self=True)
        return models.PostModel.post_manager.filter(category__in=descendant_categories)

    def get_context_data(self, **kwargs):
        """
        Переопределённый метод get_context_data().
        Передаёт в шаблон дополнительные данные.
        """
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context['category'] = category
        context['categories_list'] = models.CategoryModel.get_children(self=category)
        return context

    def get_category(self):
        """ Метод, возвращающий текущую категорию """
        if not hasattr(self, 'category'):
            self.category = models.CategoryModel.objects.get(slug=self.kwargs['category_slug'])
        return self.category


class PostPageView(DetailView):
    """ Представление страницы поста """
    model = models.PostModel
    template_name = 'blog/post_page.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """
        Переопределение метода get_object().
        Увеличивает счётчик просмотров поста при открытии.
        """
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class TagPageView(ListView):
    """ Представление страницы тега """
    model = models.PostModel
    template_name = 'blog/tag_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """
        Переопределённый метод get_queryset().
        Возвращает все посты связанные с тегом.
        """
        tag_name = self.kwargs['tag_name']
        return models.PostModel.post_manager.filter(tags__slug=tag_name).distinct()

    def get_context_data(self, **kwargs):
        """
        Переопределённый метод get_context_data().
        Передаёт в шаблон дополнительные данные.
        """
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        return context


class SearchPageView(TemplateView):
    """ Представление страницы поиска """
    template_name = 'blog/search.html'

    def get(self, request, *args, **kwargs):
        """ Метод для обработки GET-запросов """
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = models.PostModel.objects.filter(full_body__icontains=query)

            models.PostModel.objects.filter(full_body__icontains=query)

            paginator = Paginator(results, 10)
            page_number = request.GET.get('page', 1)
            results = paginator.get_page(page_number)

            context = {"query": query,
                       "results": results}

            return render(request,
                          self.template_name,
                          context)

        return render(request,
                      self.template_name,
                      {"query": request.GET['query']})
