from django.db import models
from django.utils.text import slugify

class Menu(models.Model):
    name = models.CharField(max_length=40, unique=True)
    url = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = f'/{self.name}/'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItems(models.Model):
    name = models.CharField(max_length=40)
    url = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='menu_items')

    def save(self, *args, **kwargs):
        if not self.url:
            parent_url = f'{self.parent.url}' if self.parent else None
            self.url = f'{parent_url }{self.name}/' if parent_url else f'{self.menu.url}{self.name}/'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name