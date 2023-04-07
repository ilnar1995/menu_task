from django.db import models
from .utils import ModelMixin
# Create your models here.
class Menu(ModelMixin, models.Model):
    """
    Меню
    """
    name = models.CharField('Наименование', max_length=100)
    slug = models.CharField('Слаг', max_length=255, unique=True)

    class Meta:
        db_table = 'app_menu'
        ordering = ['id']
        verbose_name_plural = 'Mеню'

class MenuItem(ModelMixin, models.Model):
    """
    Элементы меню
    """
    name = models.CharField('Наименование', max_length=100)
    slug = models.CharField('Слаг', max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

    class Meta:
        db_table = 'app_menu_item'
        ordering = ['id']
        verbose_name_plural = 'Пункты меню'
