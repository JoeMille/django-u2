# context_processors.py

from .models import Basket

def basket(request):
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
        return {'basket': basket}
    else:
        return {}