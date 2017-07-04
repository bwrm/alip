from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .forms import PhotoForm, FileForm
from .models import Photo, Product, Files


class PhotoUploadView(View):
    designer = object = None

    def get(self, request):
        prod_id = request.session.get('prod_id', None)
        if prod_id is not None:
            photos_list = Photo.objects.filter(product_id=prod_id)
            return render(self.request, 'upload/photo_upload.html', {'photos': photos_list, 'prod_id': prod_id})
        else:
            return redirect('main_site:product-add')

    def post(self, request):
        prod_id = request.session.get('prod_id', None)
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.designer = self.request.user
            if prod_id is not None:
                form.instance.product = Product.objects.get(id=prod_id)
            else:
                return redirect('main_site:product-add')
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class FilesUploadView(View):
    designer = object = None

    def get(self, request):
        prod_id = request.session.get('prod_id', None)
        if prod_id is not None:
            self.files_list = Files.objects.filter(product_id=prod_id)
            return render(self.request, 'upload/files_upload.html', {'files': self.files_list, 'prod_id': prod_id})
        else:
            return redirect('main_site:product-add')

    def post(self, request):
        prod_id = request.session.get('prod_id', None)
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.instance.designer = self.request.user
            if prod_id is not None:
                form.instance.product = Product.objects.get(id=prod_id)
            else:
                return redirect('main_site:product-add')
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def uploadsave(request):
    if request.method == 'POST':
        if request.POST['success'] == '1':
            request.session['prod_id'] = None
            return JsonResponse({'success': True})
    # self.request.session['prod_id'] = ind.id

def deletemyfile(request):
    if request.method == 'POST':
        if request.POST['id'] == '2':
            obj = Files
        elif request.POST['id'] == '1':
            obj = Photo
        else:
            return None
        filename = request.POST['file']
        deletedfile = obj.objects.get(file=filename)
        deletedfile.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

