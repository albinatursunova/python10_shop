from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    return render(request, 'product/index.html', {'categories': categories})
    #queryset(список объектов данного класса category) [category1, category2, category3]

# обработчик запроса, представление (view)
# render - принмает запрос, указывает запрос "делает всё автоматом вместо нас"
#objects - дефолтый менеджер модели
# Product.objects.all() - SELECT * FROM product;

# products/category

def products_list(request, category_slug):
    products = Product.objects.filter(category_id=category_slug)
    # SELECT * FROM product WHERE category_id = category_slug
    return render(request, 'product/products_list.html', {'products': products})

# products/id/
def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    # product = Product.objects.get(id=id)
    # SELECT * FROM product WHERE id=id LIMIT 1
    return render(request, 'product/product_details.html', {'product': product})

# class ProductDetails(View):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         return render(request, 'product/product_details.html', {'product': product})


class ProductDetails(DetailView):
    queryset = Product.objects.all()
    template_name = 'product/product_details.html'


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
