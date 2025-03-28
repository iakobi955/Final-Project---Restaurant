from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Cart, CartItem
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.core.paginator import Paginator

class RegisterPage(FormView):
  template_name = 'restaurant/register.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('login')

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super().form_valid(form)



class CustomLoginView(LoginView):
    template_name = 'restaurant/login.html'
  
    def get_success_url(self):
        return reverse_lazy('dish_list')

@login_required
def dish_list(request):
    categories = request.GET.getlist('category')
    spiciness = request.GET.get('spiciness')
    has_walnuts = request.GET.get('has_walnuts') == 'on'
    is_vegetarian = request.GET.get('is_vegetarian') == 'on'

    dishes = Dish.objects.all()

    if not categories or 'all' in categories:
        pass
    else:
        dishes = dishes.filter(category__in=categories)
    if spiciness:
        dishes = dishes.filter(spiciness_level=int(spiciness))
    if has_walnuts:
        dishes = dishes.filter(has_walnuts=True)
    if is_vegetarian:
        dishes = dishes.filter(is_vegetarian=True)

    # პაგინაცია
    paginator = Paginator(dishes, 3)  # თითოეულ გვერდზე რამდენი ელემენტი გვაქვს

    page_number = request.GET.get('page')   # გვერდის კონკრეტული ნომერი
    page_obj = paginator.get_page(page_number)  # კონკრეტული გვერდის ჩატვირთვა

    context = {
      'dishes': page_obj
  }
    return render(request, 'restaurant/dish_list.html', context)

@login_required
def add_to_cart(request, dish_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    dish = get_object_or_404(Dish, id=dish_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('dish_list')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'restaurant/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_view')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')

