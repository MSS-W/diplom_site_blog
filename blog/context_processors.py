from blog import models, forms


def get_social_links(request):
    """ Контекстный процессор, передающий во все шаблоны список ссылок """
    return {'social_links': models.SocialLinksModel.objects.all()}


def get_header_categories(request):
    """ Контекстный процессор, передающий во все шаблоны список категорий в шапке сайта """
    return {'header_categories': models.CategoryModel.objects.filter(parent__isnull=True)}


def get_search_form(request):
    """ Контекстный процессор, передающий во все шаблоны форму поиска """
    return {'search_form': forms.SearchForm()}
