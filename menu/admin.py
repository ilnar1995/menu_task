from django.contrib import admin

from .models import MenuItem, Menu
# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'menu',)
    fields = ('name', 'slug', 'parent', 'menu',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    fields = ('name', 'slug',)
    search_fields = ('name',)
    readonly_fields = ('slug',)