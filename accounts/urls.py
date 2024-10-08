from django.urls import path
from . import views
from .views.empinfo import DetailEmpInfo 
from .views.empinfo import (
    ListEmpInfo,
    CreateEmpInfo,
    UpdateEmpInfo,
    DetailEmpInfo,
    DelEmpInfo
)
app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),#註冊
    path("signin/", views.SignInView.as_view(), name="signin"),#登入
    path("signout/", views.signout, name="signout"),#退出

    path("list_emp_info/", ListEmpInfo, name="list_emp_info_click"), # list清單
    path("create_emp_info/", CreateEmpInfo, name="create_emp_info_click"), # create/add新增
    path("update_emp_info/<int:id>/", UpdateEmpInfo, name="update_emp_info_click"), # update/edit修改
    path("detail_emp_info/<int:id>/", DetailEmpInfo, name="detail_emp_info_click"), # detail詳閱
    path("del_emp_info/<int:id>/", DelEmpInfo, name="del_emp_info_click"), # del刪除

]