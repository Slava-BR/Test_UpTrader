from ..models import MenuItems
from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html')
def draw_menu(menu_name: str = None, menu_item: str = None):
    def build_menu(menu_item: str = None, submenu: list = None):
        menu = list(menu_items.filter(parent=None)) if menu_item is None \
            else list(menu_items.filter(parent__name=menu_item))
        try:
            menu.insert(menu.index(submenu[0].parent) + 1, submenu)
        except (IndexError, TypeError):
            pass
        try:
            return build_menu(menu_items.get(name=menu_item).parent.name, menu)
        except AttributeError:
            return build_menu(submenu=menu)
        except ObjectDoesNotExist:
            return menu

    menu_items = MenuItems.objects.filter(menu__name=menu_name)
    return {'menu': build_menu()} if menu_name == menu_item \
        else {'menu': build_menu(menu_item=menu_item)}