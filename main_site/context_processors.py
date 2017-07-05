from .models import Category
def category(request):
    return {'category': Category.objects.all()}