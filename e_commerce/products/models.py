from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _

from django.conf import settings
from users.models import Accounts

from mptt.models import MPTTModel, TreeForeignKey

class  Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to="category_img",null=True,blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    def __str__(self):
        return str(self.name) 

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE) 
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_img',default='/static/images/default/demo.jpg')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    favourites = models.ManyToManyField(Accounts, related_name='favourite', default=None, blank=True)

    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this product has been verified.'
            'Un-verified will not show in website.'
        ),
    )

    def __str__(self):
        return self.name
