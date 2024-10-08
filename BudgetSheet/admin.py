from django.contrib import admin
from BudgetSheet.models import *

# Create your admin here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    # fields = ('name')
    list_filter = ['name']
admin.site.register(Category, CategoryAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "symbol"]
    list_filter = ['name']
admin.site.register(Currency, CurrencyAdmin)


class BudgetSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'expenditure_items', 'estimated_quantity', 'estimated_unit_price', 'currency', 'get_estimated_expenses', 'remark_one', 'actual_quantity', 'actual_unit_price', 'get_paid', 'payer', 'remark_two')
    fields = ('category', 'expenditure_items', 'estimated_quantity', 'estimated_unit_price', 'currency', 'remark_one', 'actual_quantity', 'actual_unit_price', 'payer', 'remark_two')
    readonly_fields = ['get_estimated_expenses', 'get_paid']

    list_filter = ('category',)
    # search_fields = ('category',)
    search_fields = ('category__name', 'expenditure_items')
    ordering = ('-category',)

    # Estimated expenses：0.00
    def get_estimated_expenses(self, obj):
        return obj.estimated_expenses
    get_estimated_expenses.short_description = "預計費用支出"

    def get_paid(self, obj):
        return obj.paid
    get_paid.short_description = "已付款"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # 編輯現有對象
            return self.readonly_fields
        return []

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # 編輯現有對象
            fieldsets = list(fieldsets)
            fieldsets.append(('計算結果', {'fields': ('estimated_expenses_display', 'paid_display')}))
        return fieldsets
# 
    @property
    def estimated_expenses(self):
        if self.estimated_quantity is not None and self.estimated_unit_price is not None:
            return self.estimated_quantity * self.estimated_unit_price
        return Decimal('0.00')

    @property
    def paid(self):
        if self.actual_quantity is not None and self.actual_unit_price is not None:
            return self.actual_quantity * self.actual_unit_price
        return Decimal('0.00')
# 
admin.site.register(BudgetSheetModel, BudgetSheetAdmin)