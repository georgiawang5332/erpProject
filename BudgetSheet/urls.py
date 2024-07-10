from django.urls import path
from . import views
# from .views import (
#     PostDetailView,
# )
app_name = "budget"

# Create your urls here.
urlpatterns = [
    path("budgetSheet/", views.budgetSheetClick_view, name="budget_sheet_click"), # list
    path('createBudget/', views.createBudget, name='create_budget'),              # http://127.0.0.1:7878/posts/create
    path('<int:id>/updateBudget/', views.updateBudget, name='update_budget'),     # http://127.0.0.1:7878/posts/1/update
    path('<int:id>/deleteBudget/', views.delBudget, name='delete_budget'),               # http://127.0.0.1:7878/posts/1/delete

    path('<int:id>/detailBudget/', views.detailBudget, name='detail_budget'),

]
