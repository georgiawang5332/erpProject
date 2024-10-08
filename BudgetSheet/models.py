from django.db import models
from decimal import Decimal, InvalidOperation
from django.http import HttpResponseBadRequest


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="類別名稱")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "類別"
        verbose_name_plural = "類別"
    
class Currency(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="貨幣名稱")
    code = models.CharField(max_length=3, unique=True, verbose_name="貨幣代碼")
    symbol = models.CharField(max_length=5, verbose_name="貨幣符號", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "貨幣"
        verbose_name_plural = "貨幣"

class WeddingBudgetSheetAbstract(models.Model):
    """ WeddingBudgetSheet abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class BudgetSheetModel(WeddingBudgetSheetAbstract):
    """ WeddingBudgetSheet model """

    id                      = models.AutoField(primary_key=True, verbose_name="項目編號")
    category                = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="類別")
    expenditure_items       = models.CharField(max_length=200, verbose_name="支出項目")

    estimated_quantity      = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="預計數量", null=True, blank=True)
    estimated_unit_price    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="預計單價", null=True, blank=True) 
    currency                = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="貨幣", default=1)
    estimated_expenses = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="預計費用支出", null=True, blank=True)
    remark_one              = models.TextField( verbose_name="備註1")
 
    actual_quantity         = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="實際數量", null=True, blank=True)
    actual_unit_price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="實際單價", null=True, blank=True) 
    paid = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="已付款", null=True, blank=True)
    payer                   = models.CharField(max_length=200, verbose_name="付款人")
    remark_two              = models.TextField( verbose_name="備註2")

    # @property #no setter屬性沒有設定器
    def estimated_expenses(self):
        if self.estimated_quantity is not None and self.estimated_unit_price is not None:
            return round(self.estimated_quantity * self.estimated_unit_price, 2)
        return Decimal('0.00')

    # @property
    def paid(self):
        if self.actual_quantity is not None and self.actual_unit_price is not None:
            return round(self.actual_quantity * self.actual_unit_price, 2)
        return Decimal('0.00')

    # 添加計算預計總和的方法
    @property
    def total_estimated_expenses(self):
        # 使用您的模型字段計算總和
        return self.estimated_quantity * self.estimated_unit_price

    # 計算預計費用的總和
    def calculate_total_estimated_expenses(self):
      total = self.estimated_expenses
      return total

    def save(self, *args, **kwargs):
          # 檢查估計數量和其他數字字段是否有效
          try:
            estimated_quantity   = Decimal(self.estimated_quantity)
            estimated_unit_price = Decimal(self.estimated_unit_price)
            actual_quantity      = Decimal(self.actual_quantity)
            actual_unit_price    = Decimal(self.actual_unit_price)
          # 檢查其他數字欄位
          except InvalidOperation:
              return HttpResponseBadRequest("請提供有效的數字值。")

          # 計算預計費用支出# 在保存時更新計算字段# 計算並儲存結果
          if estimated_quantity is not None and estimated_unit_price is not None:
            self.estimated_expenses = round(estimated_quantity * estimated_unit_price, 2)
          if actual_quantity is not None and actual_unit_price is not None:
            self.paid = round(actual_quantity * actual_unit_price, 2)
            
          # 呼叫父類的 save 方法保存實例
          super().save(*args, **kwargs)

    def total_actual_expenses(self):
        # 使用您的模型字段計算總和
        total = self.actual_quantity * self.actual_unit_price
        return total

    # 貨幣千分符號格式與輸入格式
    def format_currency(self, amount):
        return "${:,.2f}".format(amount)

    @property
    def formatted_estimated_unit_price(self):
        return self.format_currency(self.estimated_unit_price)

    @property
    def formatted_estimated_expenses(self):
        return self.format_currency(self.estimated_expenses)

    @property
    def formatted_actual_unit_price(self):
        return self.format_currency(self.actual_unit_price)

    @property
    def formatted_paid(self):
        return self.format_currency(self.paid)

    # 這是之前擁有的程式    
    def __str__(self):
        return f"{self.category} - {self.expenditure_items}"

    class Meta:
        verbose_name = "婚禮預算表"
        verbose_name_plural = "婚禮預算表"
        ordering = ['-expenditure_items']

