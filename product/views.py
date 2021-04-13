# 1. Импорт из стандартной библиотеки python
# 2. Импорты из сторонних библиотек (Django, psycopg, ...)
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
# 3. Импррты из проекта
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    return render(request, 'product/index.html', {'categories': categories})
    #queryset(список объектов данного класса category) [category1, category2, category3]


class IndexPageView(ListView):
    model = Category
    template_name = 'product/index.html'
    context_object_name = 'categories'


# обработчик запроса, представление (view)
# render - принмает запрос, указывает запрос "делает всё автоматом вместо нас"
#objects - дефолтый менеджер модели
# Product.objects.all() - SELECT * FROM product;

# products/category

# def products_list(request, category_slug):
#     products = Product.objects.filter(category_id=category_slug)
#     # SELECT * FROM product WHERE category_id = category_slug
#     return render(request, 'product/products_list.html', {'products': products})

# products/category_slug/
class ProductListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'

    # Product.objects.all

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        queryset = super().get_queryset()
        # queryset -> Product.objects.all()
        queryset = queryset.filter(category_id=category_slug)
        # Product.objects.all().filter(...)
        return queryset

# products/id/
# def product_details(request, id):
#     product = get_object_or_404(Product, id=id)
#     # product = Product.objects.get(id=id)
#     # SELECT * FROM product WHERE id=id LIMIT 1
#     return render(request, 'product/product_details.html', {'product': product})

# class ProductDetails(View):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         return render(request, 'product/product_details.html', {'product': product})


class ProductDetailsView(DetailView):
    queryset = Product.objects.all()
    template_name = 'product/product_details.html'
    context_object_name = 'product'


# products/?category=...

# def products_list(request):
#     products = Product.object.all()
#     category_slug = request.GET.get('category')
#     if category_slag is not None:
#         products = products.filter(category_id=category_slug)
#     return render(request, 'product/products_list.html', {'products': products})

 # http://127.0.0.1:8000/products/?category=cellphones
# <p><a href="{% url 'products-list' cat.slug %}" >{{cat.name}}</a></p>

# TODO: переписать все вью на классы
# TODO: Сделать пагинацию списка товаров
# TODO: Сделать фильтрацию
# TODO: Сделать поиск
# TODO: Сделать верстку
# TODO: Добавить 10 товаров в катологе

# .all() - выдаёт записи из БД
# Product.objects.all()
# SELECT * FROM product;
#
# .filter(условие) - выдаёт результаты, отвечающие условиям
# Product.objects.filter(price__gt=100)
# SELECT * FROM product WHERE;

# .exclude(условия) - исключает результаты, отвечающие условию
# SELECT * FROM product WHERE NOT price > 100;
#
# .get(условия) - получает один конкретный объект
# Product.objects.get(id=2);
#
# Если по запросу не найдено ни одной записи
# DoesNotExist

# Если найдено более одной записи
# MultipleObjectsReturned
#
# .create() - метод для создания объектов модели
# Category.objects.create(name='Акссесуары', skug='accessories')
# INSERT INTO product VALUES ('Аксессуары', 'accessories');
#
# cat1 = Category(name='Аксессуары', slug='accessories')
# cat1.save()
# .update() - обновление объектов
# Product.objects.update() - для всех записей
# Product.objects.filter(...)update(...) - только для определённых записей

# Product.objects.filter(category_id='notebooks').update(price=F('price') - 1000)
# UPDATE product SET price = price - 10000 WHERE category_id = 'notebooks'

# .defer()
# .only()

# title, description, price, category_id
# Product.objects.all()
# SELECT title, description, price, category_id FROM product;
#
# title, price
# Product.objects.8only('price', 'title')
# Product.objects.defer('description', 'category_id')
# SELECT title, price FROM product;

# .order_by()
# Product.objects.oreder_by('price')
# SELECT * FROM product ORDER BY price ASC;

# Product.objects.oreder_by('-price')
# SELECT * FROM product ORDER BY price DESC;

# .all()
# Product.objects.all()
# <QuerySet[obj1, obj2, obj3, ...]>

# .values() - выдаёт поля записей ввиде словаря
# Product.objects.values()
# <QuerySet[{'id': 1, 'title': 'Apple iPhone', 'description' ...},
#           {'id': 2, 'title': 'Redmi Note 8', ...}]>
#
# Product.objects.values('title', 'price')
# <QuerySet[{'title': 'dkgkn', 'price': 654.00}
#           {'title': 'krjag', 'price': 451.00}]>
#
# .values_list()
# Product.objects.values_list()
# <QuerySet[('Apple iPhone 12', 'Lorem Ipsum', 200.00, ...)
#           ('Redmi Note 9', 'Dolor Sit amet', 250.00, ...)]>

# Product.objects.values_list('title', 'price')
# <QuerySet[('Apple iPhone 12', 'Lorem Ipsum', 200.00)
#           ('Redmi Note 9', 'Dolor Sit amet', 250.00)]>

# Product.objects.values_list('title')
# <QuerySet[('Apple iPhone 12',), ('Redmi Note 9',), ('Xiaomi Mi 10',)]

# Product.objects.values_list('title', flat=True)
# <QuerySet['Apple iPhone 12', 'Redmi Note 9', 'Xiaomi Mi 10']>

# .count() - возвращает количество результатов запроса

# Product.objects.all().count()
# Product.objects.count()
# SELECT COUNT (*) FROM product;
#
# Product.objects.filter(...).count()
# SELECT COUNT (*) FROM product WHERE ...;

# .first() - возвращает первый объект из результатов запроса
# .last() - возвращает последний объект

# Если нет ни одной записи в результатах, то возвращается None

# .exists() - проверяет, есть ли в результатах запроса хотя бы одна запись

# __gt -> ">"
# __lt -> "<"
# __gte -> ">="
# __lte -> "<="

# Product.objects.filter(price__gte=20000)

# SELECT * FROM   product WHERE price >= 20000;

# Product.objects.filter(price = 20000)
# SELECT * FROM product WHERE pice = 20000;

# __range -> BETWEEN
#
# Product.objects.filter(price__gte=20000, price__lte=50000)
# SELECT * FROM product WHERE price >= 20000 AND price <= 50000;
#
# Product.objects.filter(price__range(20000, 50000))
# SELECT * FROM product WHERE price BETWEEN 20000 AND 50000;

#  все операции на числа применяется и к датам

# exact
# iexact -> "="

# Product.object.filter(title__exact='Apple')
# SELECT * FROM product WHERE title = 'Apple';
#
# Product.object.filter(title__iexact='Apple')
# SELECT * FROM product WHERE title ILIKE 'Apple';

# stertwith
# istartwith

# Product.object.filter(title__startwith='Apple')
# SELECT * FROM product WHERE title LIKE 'Apple%';

# Product.object.filter(title__istartwith='Apple')
# SELECT * FROM product WHERE title ILIKE 'Apple%';

# endswith
# iendswith

# Product.object.filter(title__endstwith='Apple')
# SELECT * FROM product WHERE title LIKE '%Apple';
#
# Product.object.filter(title__iendstwith='Apple')
# SELECT * FROM product WHERE title ILIKE '%Apple';

# contains
# icontains

# Product.object.filter(title__contains='Apple')
# SELECT * FROM product WHERE title LIKE '%Apple%';
#
# Product.object.filter(title__icontains='Apple')
# SELECT * FROM product WHERE title LIKE '%Apple%';

# in - проверка на вхождение в список
#
# Product.object.filter(category_id__in=['notebooks', 'cellphones'])
# SELECT * FROM product WHERE categoty_id IN ('notebooks', 'cellphones');

# isnull
# Product.object.filter(image__isnull=True)
# SELECT * FROM product WHERE image IS NULL;
#
# Product.object.filter(image_isnull=False)
# SELECT * FROM product WHERE image IS NOT NULL;