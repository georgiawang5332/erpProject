from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
Pick_up_location = '接送地點'
Add_location = '追加地點'
Passengers_name = '搭乘者姓名'
Passengers_phone_num = '搭乘者電話'

PICKUP_LOCATION_CHOICES = (
    ('大學火車站', '大學火車站'),
    ('荃灣', '荃灣'),
    ('上環', '上環'),
    ('觀塘', '觀塘'),
    ('其它', '其它(不便者需求)'),
)

BridegRoom = '新郎'
Bride = '新娘'
MutualFriend = '共同朋友'

FRIEND_CHOICE = (
    (BridegRoom, '新郎'),  # 會去現場
    (Bride, '新娘'),  # 送禮人未到
    (MutualFriend, '共同友人'),  # 禮人都拒絕
)

Meat = '葷食'
Vegetarian = '素食'

DIET_CHOICE = (
    (Meat, '葷食'),  # 會去現場
    (Vegetarian, '素食'),  # 送禮人未到
)

Zero = '0'
One = '1'
Two = '2'
Three = '3'
Four = '4'

SEAT_CHOICE = (
    (Zero, '0'),
    (One, '1'),
    (Two, '2'),
    (Three, '3'),
    (Four, '4'),
)

class Invite(models.Model):
    # 對於個人邀請函
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    autono = models.AutoField(primary_key=True, verbose_name="編號")
    name = models.CharField(help_text='ex: 王小明', max_length=255, null=False, blank=False,
                            verbose_name="真實姓名")
    phone = PhoneNumberField(unique=True, default=None, null=False, blank=False, verbose_name="電話",
                             help_text='ex: +886928420424')
    address = models.CharField(help_text='ex: 台北市信義區松高路12號3樓 ', max_length=255, null=True, blank=True,
                               verbose_name="地址")
    email = models.EmailField(help_text='ex: admin123@gmail.com', max_length=255, null=True, blank=True,
                              verbose_name="信箱")
    know = models.CharField(help_text='勾選一個', max_length=4, choices=FRIEND_CHOICE,
                            verbose_name="認識新人哪位")
    diet = models.CharField(help_text='勾選一個 ', max_length=2, choices=DIET_CHOICE,
                            verbose_name="飲食偏好")
    # 專車接送
    Pick_up_location     = models.CharField(help_text='勾選一個', max_length=255, choices=PICKUP_LOCATION_CHOICES,
                            verbose_name="接送地點")
    Add_location         = models.CharField(help_text='ex: 中環 ', max_length=255, null=True, blank=True,
                               verbose_name="追加新增地址")
    Passengers_name      = models.CharField(help_text='ex: 王小明', max_length=255, null=False, blank=False,
                            verbose_name="搭乘者姓名")
    Passengers_phone_num = PhoneNumberField(unique=True, default=None, null=False, blank=False, verbose_name="電話",
                             help_text='搭乘者電話 ex: +886928420424')    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="建立時間")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="更新時間")
    status = models.BooleanField(default=True, verbose_name="狀態")
    
    # 賓客新增
    fill_multi_names = models.CharField(max_length=255, blank=True, null=True, verbose_name="多個值")
    diet_choice_non_vegetarian = models.IntegerField(default=0, verbose_name="葷食人數")
    diet_choice_vegetarian = models.IntegerField(default=0, verbose_name="素食人數")
    baby_seat = models.IntegerField(null=True, blank=True, verbose_name="嬰兒座椅數量")
    kids_count = models.IntegerField(null=True, blank=True, verbose_name="兒童數量")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 在保存時進行統計
        DietStatistics.objects.filter(id=1).update(
            vegetarian_count=models.F('vegetarian_count') + self.diet_choice_vegetarian,
            non_vegetarian_count=models.F('non_vegetarian_count') + self.diet_choice_non_vegetarian
        )

    class Meta:
        db_table = "inv_invitation"
        ordering = ('-created_at',)
        verbose_name = "邀請函"
        verbose_name_plural = "邀請函建立"

# class Invite(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     autono = models.AutoField(primary_key=True, verbose_name="編號")
#     name = models.CharField(help_text='ex: 王小明', max_length=255, null=False, blank=False,
#                             verbose_name="真實姓名")
#     phone = PhoneNumberField(unique=True, default=None, null=False, blank=False, verbose_name="電話",
#                              help_text='ex: +886928420424')
#     address = models.CharField(help_text='ex: 台北市信義區松高路12號3樓 ', max_length=255, null=True, blank=True,
#                                verbose_name="地址")
#     email = models.EmailField(help_text='ex: admin123@gmail.com', max_length=255, null=True, blank=True,
#                               verbose_name="信箱")
#     know = models.CharField(help_text='勾選一個', max_length=4, choices=FRIEND_CHOICE,
#                             verbose_name="認識新人哪位")
#     diet = models.CharField(help_text='勾選一個 ', max_length=2, choices=DIET_CHOICE,
#                             verbose_name="飲食偏好")
#     baby_seat = models.CharField(help_text='勾選一個 ', max_length=1, choices=SEAT_CHOICE,
#                                  verbose_name="嬰兒座椅數量")
#     created_at = models.DateTimeField(default=timezone.now, verbose_name="建立時間")
#     updated_at = models.DateTimeField(default=timezone.now, verbose_name="更新時間")
#     status = models.BooleanField(default=True, verbose_name="狀態")

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = "inv_invitation"
#         ordering = ('-created_at',)
#         verbose_name = "邀請函"
#         verbose_name_plural = "邀請函建立"
# 飲食統計
class DietStatistics(models.Model):
    vegetarian_count = models.IntegerField(default=0, verbose_name="素食人數")
    non_vegetarian_count = models.IntegerField(default=0, verbose_name="葷食人數")
 

class GiveMoney(models.Model):
    autonoGive = models.AutoField(primary_key=True, verbose_name="編號")
    nameGive = models.CharField(help_text='ex: 王小明', max_length=255, null=True, blank=True,
                                verbose_name="真實姓名")
    phoneGive = PhoneNumberField(unique=True, default=None, null=False, blank=False, verbose_name="電話",
                                 help_text='ex: +886928420424')
    addressGive = models.CharField(help_text='ex: 台北市信義區松高路12號3樓 ', max_length=255, null=True, blank=True,
                                   verbose_name="地址")
    emailGive = models.EmailField(help_text='ex: admin123@gmail.com', max_length=255, null=True, blank=True,
                                  verbose_name="信箱")
    status = models.BooleanField(default=True, verbose_name="狀態")

    def __str__(self):
        return self.nameGive

    class Meta:
        db_table = "inv_givemoney"
        ordering = ('-phoneGive',)
        verbose_name = "給禮金"
        verbose_name_plural = "給禮金建立"


class NotAttend(models.Model):
    autonoNo = models.AutoField(primary_key=True, verbose_name="編號")
    nameNo = models.CharField(help_text='ex: 王小明', max_length=255, null=True, blank=True,
                              verbose_name="真實姓名")
    emailNo = models.EmailField(help_text='ex: admin123@gmail.com', max_length=255, null=True, blank=True,
                                verbose_name="信箱")
    msgNo = models.CharField(help_text='ex: 給新人一段祝福語 ', max_length=255, null=True, blank=True,
                             verbose_name="留言")
    status = models.BooleanField(default=True, verbose_name="狀態")

    def __str__(self):
        return self.nameNo

    class Meta:
        db_table = "inv_notattend"
        ordering = ('-emailNo',)
        verbose_name = "拒絕參加留言板"
        verbose_name_plural = "留言板 建立"
