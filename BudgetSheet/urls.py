from django.urls import path
from . import views
# from .views import (
#     PostDetailView,
# )
app_name = "budget"

# Create your urls here.
urlpatterns = [
    path("budget-sheet/", views.ListBudgetSheetClick, name="budget_sheet_click"), # list 婚禮
    path('create-budget/', views.createBudget, name='create_budget'),              # http://127.0.0.1:7878/posts/create
    path('<int:id>/updateBudget/', views.updateBudget, name='update_budget'),     # http://127.0.0.1:7878/posts/1/update
    path('<int:id>/deleteBudget/', views.delBudget, name='delete_budget'),        # http://127.0.0.1:7878/posts/1/delete
    path('<int:id>/detailBudget/', views.detailBudget, name='detail_budget'),

    path('list-category/', views.ListCategoryClick, name="list_category"),         # list 類別category http://127.0.0.1:7878/posts/list
    path('create-category/', views.CreateCategory, name='create_category'),        # http://127.0.0.1:7878/posts/create
    path('<int:id>/detailCategory/', views.detailCategory, name='detail_category'),# http://127.0.0.1:7878/posts/1/detail
    path('<int:id>/updateCategory/', views.updateCategory, name='update_category'),# http://127.0.0.1:7878/posts/1/update
    path('<int:id>/deleteCategory/', views.delCategory, name='delete_category'),   # http://127.0.0.1:7878/posts/1/delete

    path('list-currency/', views.ListCurrencyClick, name="list_currency"),           # list 貨幣currency http://127.0.0.1:7878/posts/list
    path('create-currency/', views.CreateCurrency, name='create_currency'),          # http://127.0.0.1:7878/posts/create
    path('<int:id>/detail-currency/', views.detailCurrency, name='detail_currency'), # http://127.0.0.1:7878/posts/1/detail
    path('<int:id>/update-currency/', views.updateCurrency, name='update_currency'), # http://127.0.0.1:7878/posts/1/update
    path('<int:id>/delete-currency/', views.delCurrency, name='delete_currency'),    # http://127.0.0.1:7878/posts/1/delete

]