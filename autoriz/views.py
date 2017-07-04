from django.shortcuts import render,redirect, HttpResponseRedirect
from .forms import UserForm, TypeServiceForm
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import MyUser, CncService, Producer
from django.core.urlresolvers import reverse_lazy
from main_site.models import Product
from upload.models import Photo
from .forms import CutomProducerForm, PlainUserAccountForm
from django.http import QueryDict
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            user = uf.save(commit=False)
            username = uf.cleaned_data['email']
            # TODO: checking for existing username
            # TODO: bound when password1 and password2 doesnt match
            password = uf.cleaned_data['password']
            password2 = request.POST['password2']
            if password and password != password2:
                uf = UserForm()
                return render(request, 'registration/signup.html', {'form': uf, 'passvalid':True})
            user.set_password(password)
            user.save()
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                pass
    else:
        uf = UserForm()
    return render(request, 'registration/signup.html', {'form' : uf})

class MyAccountView(LoginRequiredMixin, TemplateView):
    model = MyUser
    template_name = 'registration/myaccount.html'



class PlainUser(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = PlainUserAccountForm
    template_name = 'registration/plainuseraccaunt.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('autoriz:myaccount-home')

class BelongingToProducerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Producer').exists() or user.is_superuser


class AllUsersProduct(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'registration/usersproducts.html'
    context_object_name = 'grouped_products'

    def get_queryset(self):
        base_qs = super(AllUsersProduct, self).get_queryset()
        if self.request.user.is_superuser:
            return base_qs.all()
        else:
            return base_qs.filter(designer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(AllUsersProduct,self).get_context_data(**kwargs)
        context['images'] = Photo.objects.filter(designer=self.request.user)
        return context


class ProducerReg(LoginRequiredMixin, CreateView):
    model = Producer
    form_class = CutomProducerForm
    template_name = 'registration/producerregistration.html'
    success_url = reverse_lazy('main_site:index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_producer:
            return redirect('main_site:index')
        else:
            r = Producer.objects.filter(user=self.request.user)
            if self.request.user.is_producer == False and r.__len__() == 1:
                return HttpResponse('<h2>Your zaiavka na rassmotrenii v bligaishee vremia ona budet obrbotana</h2>')
            else:
                return super(ProducerReg, self).get(request, *args, **kwargs)

class TypeService(CreateView):

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('services') == '1':
            return redirect('autoriz:cnc-service')
        return super(TypeService, self).get(request, *args, **kwargs)

    form_class = TypeServiceForm
    template_name = 'registration/addservice.html'

class CncReg(CreateView):
    model = CncService
    template_name = 'registration/addservice.html'
    fields = '__all__'


class ProductsProducedByMe(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'registration/usersproducts.html'
    context_object_name = 'grouped_products'

    def get_queryset(self):
            return Product.objects.filter(producers__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProductsProducedByMe,self).get_context_data(**kwargs)
        context['images'] = Photo.objects.filter(designer=self.request.user)
        return context