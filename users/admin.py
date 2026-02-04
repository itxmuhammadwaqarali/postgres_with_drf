from django.contrib import admin
from .models import User
from products.models import Product
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'size', 'available', 'rating', 'color', 'created_at')
    list_filter = ('available', 'size', 'color')
    search_fields = ('name', 'description')
