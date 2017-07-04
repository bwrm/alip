from django.views.generic import CreateView, ListView
from .models import Review
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from main_site.models import Product
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateReview(CreateView, LoginRequiredMixin):
    model = Review
    form_class = ReviewForm
    template_name = 'review/create.html'
    success_url = reverse_lazy('main_site:products')
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.item = get_object_or_404(Product, slug=self.kwargs['slug'])
        self.object.save()
        return super(CreateReview, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateReview, self).get_context_data(**kwargs)
        if self.kwargs['slug'] == None:
            reverse_lazy('main_site:products')
        else:
            context['product'] = get_object_or_404(Product, slug=self.kwargs['slug'])
        return context
# TODO: add comment posting date

class ReviewListView(ListView):
    model = Review
    template_name = 'review/list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        self.item = get_object_or_404(Product, slug=self.kwargs['slug'])
        return Review.objects.filter(item=self.item, is_published=True)

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        if self.kwargs['slug'] == None:
            reverse_lazy('main_site:products')
        else:
            context['product'] = get_object_or_404(Product, slug=self.kwargs['slug'])
        return context
