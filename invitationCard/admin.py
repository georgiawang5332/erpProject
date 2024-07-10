from django.contrib import admin

from invitationCard.models import Invite, GiveMoney, NotAttend


# Register your models here.
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'autono', 'name', 'phone', 'address', 'email', 'know', 'diet', 'baby_seat', 'created_at', 'updated_at'
    )
    fields = (
        'name', 'phone', 'address', 'email', 'know', 'diet', 'baby_seat', 'created_at', 'updated_at'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('-created_at',)


admin.site.register(Invite, InviteAdmin)


class GiveMoneyAdmin(admin.ModelAdmin):
    list_display = (
        'autonoGive', 'nameGive', 'phoneGive', 'addressGive', 'emailGive',
    )
    fields = (
        'nameGive', 'phoneGive', 'addressGive', 'emailGive',
    )
    list_filter = ('nameGive',)
    search_fields = ('nameGive',)
    ordering = ('-emailGive',)


admin.site.register(GiveMoney, GiveMoneyAdmin)


class NotAttendAdmin(admin.ModelAdmin):
    list_display = (
        'autonoNo', 'nameNo', 'emailNo', 'msgNo',
    )
    fields = (
        'nameNo', 'emailNo', 'msgNo',
    )
    list_filter = ('nameNo',)
    search_fields = ('nameNo',)
    ordering = ('-emailNo',)


admin.site.register(NotAttend, NotAttendAdmin)
