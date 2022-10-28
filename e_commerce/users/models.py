from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _

from django.core.validators import RegexValidator 
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


class Accounts(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    phone_regex = RegexValidator(regex=r'^(?:\+88|88)?(01[3-9]\d{8})$', message="Phone number must be entered in the format: '+8801XXXXXX'. Up to 14 digits allowed.")
    mobile_number = models.CharField(validators=[phone_regex], max_length=20, unique=True,null=True,blank=True)

    is_verified = models.BooleanField(
        _('verified'),
        default=False, 
        help_text=_(
            'Designates whether this user has been verified.'
            'Un-verified users cannot log in.'
        ),
    )

    is_saler = models.BooleanField(
        _('Saler Permission'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as founder.'
        ),
    )

    created_at = models.DateTimeField(default=now, editable=False)
    ##default
    profile_pic = models.FileField(upload_to='profile_pic',null=True,blank=True)
    address = models.TextField(null=True,blank=True)


    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email

    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Users'