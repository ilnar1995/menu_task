# создание пользовательских тэгов
from django import template
from menu.models import MenuItem, Menu
from menu.utils import item_tree

register = template.Library() #создаем экземпляр класса library через котор происходит регистрация собственных шаблонных тэгов



@register.inclusion_tag(
    'menu/menu.html')
def draw_menu(menu_slug=None, path_list=None):
    items = list(MenuItem.objects.filter(menu__slug=menu_slug).values())
    tree = item_tree(items)
    return {"instance": tree, "menu_slug": menu_slug, "path_list": path_list}