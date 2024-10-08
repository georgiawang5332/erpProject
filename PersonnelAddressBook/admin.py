from django.contrib import admin
from PersonnelAddressBook.models import *

# Register your models here.
class EmploymentStatusAdmin(admin.ModelAdmin):
    list_display = ['status', 'description']
admin.site.register(EmploymentStatus, EmploymentStatusAdmin) 

class GenderAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Gender, GenderAdmin) 

class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['status']
admin.site.register(MaritalStatus, MaritalStatusAdmin) 

class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['level']
admin.site.register(EducationLevel, EducationLevelAdmin) 

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Department, DepartmentAdmin) 

class EmploymentCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
admin.site.register(EmploymentCategory, EmploymentCategoryAdmin) 

class RecruitmentSourceAdmin(admin.ModelAdmin):
    list_display = ['source']
admin.site.register(RecruitmentSource, RecruitmentSourceAdmin) 

class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('dataNum', 'jobNum', 'employeeAccount')
    list_display = ['dataNum','name', 'engName', 'ID_Card', 'dateOfBirth', 'age', 'gender', 'maritalStatus', 'highestEduLev', 'OTJStatus', 'jobNum', 'employeeAccount', 'immediateSupervisor', 'grade', 'empCategory', 'recruitmentSource', 'companyPhone', 'extension', 'companyMobilePhone', 'companyMailbox', 'startDate', 'resignationDate', 'remark'] # 在列表中顯示年齡 正確：明確列出所有字段

    def get_readonly_fields(self, request, obj=None):
        if obj:  # 編輯現有對象 
            return self.readonly_fields + ('dataNum', 'jobNum', 'employeeAccount')
        return self.readonly_fields  # 建立新對象
    
    def save_model(self, request, obj, form, change):
        if not change:  # 建立新物件時
            # 這裡可以產生 employeeAccount，如果需要的話
            obj.employeeAccount = self.generate_employee_account(obj)
        super().save_model(request, obj, form, change)
    
    def generate_employee_account(self, obj):
        # 確保 name 和 engName 不為空
        name = obj.name if obj.name else "Unknown"
        engName = obj.engName if obj.engName else "Unknown"
        # 實作產生員工帳號的邏輯
        # 這只是一個範例，您需要根據自己的需求修改
        return f"{engName}" # return f"{obj.name}_{obj.jobNum}"
    
admin.site.register(Employee, EmployeeAdmin) 


class GroupEmailAdmin(admin.ModelAdmin):
    list_display = ['number', 'employee', 'action', 'added_at'] # 在列表中顯示年齡 正確：明確列出所有字段

admin.site.register(GroupEmail, GroupEmailAdmin) 

# 信件寄送
class SendEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "message", "from_email", "to_email"]
    list_filter = ['subject']
admin.site.register(SendEmail, SendEmailAdmin)