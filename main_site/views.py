from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, ContextMixin, View, TemplateResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from autoriz.models import MyUser as User
from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from .models import Product, DetailProduce, OurProfit
from categories.models import Category
from autoriz.models import Producer
from upload.models import Photo, Files
from django.http import QueryDict
from .forms import ProdForm, ProductProduceForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.template.defaultfilters import slugify
from cart.forms import CartAddProductForm
from django.utils.translation import ugettext_lazy as _
from django.db.models import Min, Max
from unidecode import unidecode

class Prices:
    """class that calculate all products costs"""
    def get_end_price(self, product_id):
        self.designers = get_object_or_404(Product, id=product_id).designer_price
        self.our = get_object_or_404(OurProfit, id=1).profit
        self.producers = get_object_or_404(DetailProduce, product_id=product_id).price
        self.finish = round(float(self.designers + self.producers)*(self.our/100+1), 2)
        return self.finish

class IndexView(TemplateView):
    template_name = 'main_site/index.html'


class GoodListView(ListView):
    model = Product
    template_name = 'main_site/prod-4-col.html'
    context_object_name = 'grouped_products'
    queryset = Product.objects.filter(available=True)
    img_conteiner = []

    def get_context_data(self, **kwargs):
        context = super(GoodListView,self).get_context_data(**kwargs)
        for i in self.queryset:
            temp_obj = Product.objects.get(pk=i.id)
            self.img_conteiner.append(temp_obj.photo_set.first())
        context['img'] = self.img_conteiner
        return context

class ProdDetailView(DetailView):
    """
    This class used for showing product page from catalog.
    """
    model = Product
    template_name = 'main_site/prod-page.html'

    def get_context_data(self, **kwargs):
        # TODO: change searching product by slug to pk
        self.pk = self.kwargs.get('slug', None)
        self.prod = Product.objects.get(slug=self.pk)
        context = super(ProdDetailView,self).get_context_data(**kwargs)
        current_object = DetailProduce.objects.filter(product_id=self.prod.pk)
        avprice = current_object.aggregate(Min('price'), Max('price'))
        endprice = Prices()
        context['endprice'] = endprice.get_end_price(self.prod.pk)
        context['category'] = Category.objects.all()
        context['minprice'] = avprice['price__min']
        context['maxprice'] = avprice['price__max']
        context['cart_form'] = CartAddProductForm()
        try:
            #check if user alredy produce product
            DetailProduce.objects.get(product_id=self.prod.pk, producer_id=self.request.user.id)
            context['alredy_produce'] = True
        except:
            pass
        related=[]
        for i in Product.objects.filter()[:4]:
            related.append(i)
        context['related'] = related
        context['count_producers'] = DetailProduce.objects.filter(product_id=self.prod.pk).count()
        return context


class ProdCatView(ListView):
    template_name = 'main_site/prod-4-col.html'
    model = Product
    context_object_name = 'grouped_products'

    def get_queryset(self, **kwargs):
        if self.kwargs['category'] == None:
            self.cat = Product.objects.filter(available=True)
        else:
            self.cat = Product.objects.filter(
                category_id=Category.objects.get(slug=self.kwargs['category']).id,
                available=True
            )
        return self.cat
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ProdCatView, self).get_context_data(**kwargs)
    #     return context

def sometest(request):
    all_data = request.GET
    all = QueryDict('name=John&lastname=Smith')
    return render(request, 'main_site/test.html', {'all_data':all_data.getlist('mytext'), 'all': all})


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProdForm
    template_name = 'main_site/product_form.html'
    success_url = reverse_lazy('upload:photo_upload')
    designer = object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.designer = self.request.user
        self.object.slug = slugify(unidecode(self.request.POST.get('name')))
        self.object.available = True
        myuserobj = User.objects.get(email=self.request.user)
        myuserobj.is_designer = True
        myuserobj.save()
        self.object.save()
        self.ind = Product.objects.get(slug=self.object.slug, designer=self.object.designer)
        self.request.session['prod_id'] = self.ind.id
        #TODO: add error to form validation if slug not unique for current user
        return super(ProductCreate, self).form_valid(form)


class ProductUpdate(LoginRequiredMixin, UpdateView):
    #TODO: back button to product on uploading photo page
    model = Product
    fields = ['category', 'name', 'description','designer_price', 'available']
    success_url = reverse_lazy('upload:photo_upload')
    designer = object = None

    def get_queryset(self):
        base_qs = super(ProductUpdate, self).get_queryset()
        if self.request.user.is_superuser:
            return base_qs.all()
        else:
            return base_qs.filter(designer=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.designer = self.request.user
        self.object.save()
        self.ind = Product.objects.get(pk=self.request.POST.get('id'))
        self.request.session['prod_id'] = self.ind.id
        self.request.session['prod_cat'] = self.ind.category.slug
        self.request.session['prod_slug'] = self.ind.slug
        return super(ProductUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['prod_cat'] = self.request.session.get('prod_cat', None)
        context['prod_slug'] = self.request.session.get('prod_slug', None)
        return context


class ProductDelete(LoginRequiredMixin, DeleteView):
    # TODO: doesnt work delete conformation
    model = Product
    success_url = reverse_lazy('main_site:products')
    # template_name = 'product_confirm_delete.html'


class ProducerListView(ListView):
    model = User
    template_name = 'main_site/map.html'
    context_object_name = 'producer_list'

class ProductProduce(CreateView):
    model = DetailProduce
    form_class = ProductProduceForm
    template_name = 'main_site/can-produce-pub.html'
    object = None

    def get_success_url(self):
        self.curprod = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return reverse_lazy('main_site:product',
                            kwargs={'category': self.curprod.category.slug, 'slug': self.curprod.slug})

    #TODO: chek if user alredy producer

    def get(self, request, *args, **kwargs):
        self.pk = self.kwargs.get('pk', None)
        try:
            DetailProduce.objects.get(product_id=self.pk, producer_id=self.request.user.id)
            # return redirect('main_site:products')
            return HttpResponse('You are alredy produce this product')
        except:
            pass
        return super(ProductProduce, self).get(request, *args, **kwargs)


    def form_valid(self, form):
        if self.request.POST.get('agree', None) == '1':
            self.object = form.save(commit=False)
            self.pk = self.kwargs.get('pk', None)
            self.object.producer = self.request.user
            self.object.product = Product.objects.get(pk=self.pk)
            self.object.save()
        else:
            return HttpResponse('Back and agree with our conditions')
        return super(ProductProduce, self).form_valid(form)


class ProductProduceSet(UpdateView):
    model = DetailProduce
    fields = ['price', 'days', 'shipping']
    template_name = 'main_site/can-produce-pub.html'

    def get_success_url(self):
        self.curprod = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return reverse_lazy('main_site:product', kwargs={'category': self.curprod.category.slug, 'slug': self.curprod.slug})

    def get_object(self, queryset=None):
        obj = get_object_or_404(DetailProduce, producer_id=self.request.user.id, product_id=self.kwargs.get('pk'))
        return obj


    # form_class = ProductProduceForm
    # template_name = 'main_site/can-produce-pub.html'
    # object = None
    # success_url = reverse_lazy('main_site:products')
    # #TODO: reverse to previos product page and chek if user alredy producer
    #
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.pk = self.kwargs.get('pk', None)
    #     self.prod = Product.objects.get(pk=self.pk)
    #     self.object.producer = self.request.user
    #     self.object.product = Product.objects.get(pk=self.pk)
    #     self.object.save()
    #     return super(ProductProduceSet, self).form_valid(form)

class CancelProduce(TemplateView):
    template_name = 'main_site/cancel-produce.html'

    # def get(self, request, *args, **kwargs):
    #     self.pk = self.kwargs.get('pk', None)
    #     self.prod = Product.objects.get(pk=self.pk)
    #     if self.request.GET.get('agree', None) == '1':
    #         self.prod.producers.remove(Producer.objects.get(user=self.request.user))
    #         # self.prod.save()
    #         return redirect('main_site:products')
    #     return super(CancelProduce, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CancelProduce, self).get_context_data(**kwargs)
        # context['product'] = self.prod
        return context
