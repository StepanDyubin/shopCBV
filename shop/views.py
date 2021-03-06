from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_protect



from blog.views import CategoryListView


from .models import Category, Product, ProductType


# Create your views here.
class ProductListView(ListView):
    template_name = "shop/product_list.html"
    model = Product

    paginate_by = 10

    def get_queryset(self):
        queryset_list = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            return queryset_list.filter(Q(title__icontains=query)).distinct()
        else:
            return queryset_list


class ItemListView(ProductListView):
    context_object_name = 'products'

    def get_queryset(self):
        """ Нужно сделать создав метод для Queryser """
        queryset_list = Product.objects.items()
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:10]
        return context


class ServiceListView(ProductListView):
    template_name = "shop/service_list.html"
    context_object_name = 'services'

    def get_queryset(self):
        """ Нужно сделать создав метод для Queryser """
        queryset_list = Product.objects.services()
        return queryset_list


class CategoryShopListView(CategoryListView):
    template_name = "shop/category_list.html"


class ItemCategoriedListView(ItemListView):
    def get_queryset(self):
        queryset_list = super(ItemCategoriedListView, self).get_queryset()
        return queryset_list.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super(ItemCategoriedListView, self).get_context_data(**kwargs)
        context['another_categories'] = Category.objects.all()[:10]
        context['category_slug'] = self.kwargs['category_slug']
        return context


class ProductDetalilView(DetailView):
    model = Product
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ProductDetalilView, self).get_context_data(**kwargs)
        item = context['item']
        related_items = Product.objects.items().filter(relation=item).distinct()
        related_services = Product.objects.services().filter(relation=item).distinct()
        context['related_items'] = related_items
        context['related_services'] = related_services
        return context


class ItemDetailView(ProductDetalilView):
    template_name = "shop/product_detail.html"


class ServiceDetailView(ProductDetalilView):
    template_name = "shop/service_detail.html"
