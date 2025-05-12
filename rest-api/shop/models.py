from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import Media
from account.models import User
from .validators import validate_telegram_url
        
        
class BaseTranslatableModel(models.Model):
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_uk = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    
    desc_uz = models.CharField(max_length=500, null=True, blank=True)
    desc_en = models.CharField(max_length=500, null=True, blank=True)
    desc_uk = models.CharField(max_length=500, null=True, blank=True)
    desc_ru = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        abstract = True

    def get_title(self, language_code):
        return getattr(self, f'title_{language_code}', self.title_uz)

    def get_description(self, language_code):
        return getattr(self, f'desc_{language_code}', self.desc_uz)
    
        
class Shop(BaseTranslatableModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='shops')
    image = models.OneToOneField(to=Media, on_delete=models.CASCADE, null=True, blank=True)
    telegram_link = models.URLField(validators=[validate_telegram_url])

    def __str__(self) -> str:
        return self.get_title('uz') or "No Title"
    
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class Category(BaseTranslatableModel):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    image = models.OneToOneField(to=Media, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.get_title('uz') or "No Title"
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(BaseTranslatableModel):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    image = models.OneToOneField(to=Media, on_delete=models.CASCADE, null=True, blank=True)
    price = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return self.get_title('uz') or "No Title"
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")