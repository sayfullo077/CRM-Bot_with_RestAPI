from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from common.models import Media


class User(AbstractUser):
    class RoleType(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        SELLER = "seller", _("Seller")
    username = models.CharField(_("username"), max_length=123, null=True, blank=True, unique=True)
    fullname = models.CharField(_("fullname"), max_length=123, null=True, blank=True)
    firstname = models.CharField(_("firstname"), max_length=123, null=True, blank=True)
    lastname = models.CharField(_("lastname"), max_length=123, null=True, blank=True)
    photo = models.ForeignKey(
        Media, on_delete=models.SET_NULL, null=True, blank=True, related_name="photo"
    )
    language = models.CharField(_("language"), max_length=5, default='uz')
    telegram_id = models.CharField(_("telegram id"), max_length=55, unique=True)
    phone_number = models.CharField(_("phone number"), max_length=30, null=True, blank=True, unique=True)
    password = models.CharField(_("password"), max_length=125, null=True, blank=True)
    role = models.CharField(_("role"), choices=RoleType.choices, max_length=55, default=RoleType.CUSTOMER)
    ordered = models.BooleanField(default=False)
    notification = models.BooleanField(default=True)
    created_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        if self.phone_number:
            return f"{self.phone_number} {self.username} ({self.telegram_id})"
        return f"{self.email}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
        
class Groups(models.Model):
    name = models.CharField(_("name"), max_length=100)
    users = models.ManyToManyField(User, related_name="user_groups", blank=True)
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")