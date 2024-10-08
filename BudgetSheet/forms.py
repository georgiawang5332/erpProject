from django import forms
from .models import *

# Create your models here.
class BudgetSheetForm(forms.ModelForm):
  class Meta:
    model = BudgetSheetModel
    fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # fields = ['name']  # 假設 Category 模型有一個 name 字段
        fields = '__all__'