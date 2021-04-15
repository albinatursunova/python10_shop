# 1. Импорт из стандартной библиотеки python
# 2. Импорты из сторонних библиотек (Django, psycopg, ...)
import django_filters
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
# 3. Импррты из проекта
from .models import Category, Product
from django_filters.views import FilterView


def index(request):
    categories = Category.objects.all()
    return render(request, 'product/index.html', {'categories': categories})
    #queryset(список объектов данного класса category) [category1, category2, category3]


class IndexPageView(ListView):
    model = Category
    template_name = 'product/index.html'
    context_object_name = 'categories'

class ProductFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter('price', 'gte')
    price_to = django_filters.NumberFilter('price', 'lte')

    class Meta:
        model = Product
        fields = ['price_from', 'price_to']


# обработчик запроса, представление (view)
# render - принмает запрос, указывает запрос "делает всё автоматом вместо нас"
#objects - дефолтый менеджер модели
# Product.objects.all() - SELECT * FROM product;

# products/category_slug/
class ProductListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'
    paginate_by = 10 #pagination
    # products/category?price_from=1000&price_to=2000

    # Product.objects.all

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        queryset = super().get_queryset()
        # queryset -> Product.objects.all()
        queryset = queryset.filter(category_id=category_slug)

        # фильтрация
        queryset = ProductFilter(self.request.GET, queryset=queryset).qs

        # сортировка
        # product/category/?sort=price_asc
        sort = self.request.GET.get('sort')
        sort_choices = {'price_asc': 'price', 'price_desc': '-price', 'title_asc': 'title', 'title_desc': '-title'}
        sort = sort_choices.get(sort)
        if sort:
            queryset = queryset.order_by(sort)

        # Product.objects.all().filter(...)
        return queryset


class ProductDetailsView(DetailView):
    queryset = Product.objects.all()
    template_name = 'product/product_details.html'
    context_object_name = 'product'


# TODO: переписать все вью на классы
# TODO: Сделать пагинацию списка товаров
# TODO: Сделать фильтрацию
# TODO: Сделать поиск
# TODO: Сделать верстку
# TODO: Добавить 10 товаров в катологе