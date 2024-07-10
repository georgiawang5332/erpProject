from django import forms
from .models import *

# Create your models here.
class BudgetSheetForm(forms.ModelForm):
  class Meta:
    model = BudgetSheetModel
    fields = '__all__'

