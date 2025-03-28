from django.contrib import admin
from .models import Dish, Cart, CartItem

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'spiciness_level', 'has_walnuts', 'is_vegetarian', 'price')
    list_filter = ('category', 'spiciness_level', 'has_walnuts', 'is_vegetarian')
    search_fields = ('name',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_price')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('dish', 'cart', 'quantity', 'total_price')
