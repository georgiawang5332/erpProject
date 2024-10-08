from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """ User manager """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email Address field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    from django.contrib.auth.models import Group, Permission
    # 用戶分配群組和權限
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='%(class)s_groups',  # 修改這裡的related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='%(class)s_user_permissions',  # 修改這裡的related_name
        related_query_name="user",
    )
    email = models.EmailField(
        _("信箱帳號"),
        max_length=255,
        unique=True,
        help_text="Ex: example@example.com",
    )
    username = models.CharField(
        _("名稱"),
        max_length=255,
        unique=True,
        help_text="你的全名",
        null=True, blank=True
    )

    first_name = models.CharField(_("姓氏"), max_length=30, blank=True)
    last_name = models.CharField(_("名字"), max_length=30, blank=True)
    avatar = models.ImageField(_("頭像"), upload_to='avatars/', null=True, blank=True, )
    
    is_staff = models.BooleanField(_("Staff status員工狀況"), default=False)
    is_active = models.BooleanField(_("Active積極的"), default=True)
    date_joined = models.DateTimeField(_("Date Joined加入日期"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated最後更新"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # 使用 email 作為 USERNAME_FIELD
    # REQUIRED_FIELDS = ["username"]  # 創建superuser時要求填寫的字段
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "使用者"
        verbose_name_plural = "使用者"