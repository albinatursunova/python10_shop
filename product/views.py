# 1. Импорт из стандартной библиотеки python
# 2. Импорты из сторонних библиотек (Django, psycopg, ...)
import django_filters
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, DeleteView
# 3. Импорты из проекта
from .forms import CreateProductForm, ImageFormSet
from .models import Category, Product, ProductImage


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
    paginate_by = 3 #pagination
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




class CreateProductView(View):
    def get(self, request):
        form = CreateProductForm()
        images_form = ImageFormSet(queryset=ProductImage.objects.none())
        return render(request, 'products/create.html', locals())

    def post(self, request):
        form = CreateProductForm(request.POST)
        images_form = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and images_form.is_valid():
            product = form.save()
            for i_form in  images_form:
                image = i_form.get('image')
                if image is not None:
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            return redirect(product.get_absolute_url())
        print(form.errors, images_form.errors)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('index-page')

class ProductEditView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(isinstance=product, data=request.POST)
        images_form = ImageFormSet(queriset=product.images.all())
        return render(request, 'product/edit.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(isinstance=product, data=request.POST)
        images_form = ImageFormSet(request.POST, request.FILES, queriset=product.images.all())
        if form.is_valid() and images_form.is_valid():
            product = form.save()
            for i_from in images_form.cleaned_data:
                image = form.get('image')
                if image is not None and ProductImage.objects.filter(product=product, image=image).exists():
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            for i_form in images_form.deleted_forms:
                image = i_form.cleaned_data.get('id')
                if image is not None:
                    image.delete()
            return redirect(product.get_absolute_url())
        print(form.errors, images_form.errors)
