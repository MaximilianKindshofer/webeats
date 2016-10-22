from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import User_extend
from meals.models import Dish
from .models import Favourite
from .secret import client_id
from django.views.decorators.csrf import csrf_exempt
import random
from .wunderlist_utils import get_authorization_url, make_api_call
def register(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.save()
        User_extend.objects.create(user=user)
        return redirect('login')
    return render(request, 'profiles/registration.html', { 'form': form })

def fav_toggle(request, pk):

    dish = get_object_or_404(Dish, pk=pk)
    if dish not in request.user.user_extend.get_favourites(): 
        Favourite.objects.create(user=request.user.user_extend,
                                 dish=dish)
    else:
        fav = Favourite.objects.filter(user=request.user.user_extend).get(dish=dish)
        fav.delete()
    return redirect('meals:dish_detail', dish.pk)

def request_token(request):
    state = random.randint(1,100)
    user = request.user.user_extend
    user.state = state
    user.save()
    redirect_url = 'https://bithive.space/profiles/get_token'
    return redirect(get_authorization_url(client_id,redirect_url,state))
    
def get_token(request):

    state = request.GET.get('state')
    if state != request.user.user_extend.state:
        raise SuspiciousOperation
    else:
        code = request.GET.get('code')
        token = make_api_call(code)
        return render(request, 'profiles/test.html', {'test': token})
        

