from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
# relativedelta 是 Python dateutil 模塊中的一個類，該類用於處理與日期相關的操作。
# relativedelta 提供了一個靈活的方式來進行日期計算，允許你添加或減去年、月、日等時間單位。

# Create your models here.
class EmploymentStatus(models.Model):
    status = models.CharField(max_length=20, unique=True, verbose_name="狀態")
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "在職狀態"
        verbose_name_plural = "在職狀態"

class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="性別")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "性別"
        verbose_name_plural = "性別"

class MaritalStatus(models.Model):
    status = models.CharField(max_length=50, unique=True, verbose_name="婚姻狀態")
    
    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "婚姻狀態"
        verbose_name_plural = "婚姻狀態"

class EducationLevel(models.Model):
    level = models.CharField(max_length=100, unique=True, verbose_name="教育程度")
    
    def __str__(self):
        return self.level
    
    class Meta:
        verbose_name = "教育程度"
        verbose_name_plural = "教育程度"

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="部門名稱")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "部門名稱"
        verbose_name_plural = "部門名稱"

class EmploymentCategory(models.Model):
    category = models.CharField(max_length=50, unique=True, verbose_name="聘僱類別")
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = "聘僱類別"
        verbose_name_plural = "聘僱類別"

class RecruitmentSource(models.Model):
    source = models.CharField(max_length=50, unique=True, verbose_name="招聘來源")
    
    def __str__(self):
        return self.source
    
    class Meta:
        verbose_name = "招聘來源"
        verbose_name_plural = "招聘來源"

class Employee(models.Model):
    dataNum       = models.CharField(max_length=30, unique=True, verbose_name="資料編號")
    name          = models.CharField(max_length=100,  verbose_name="姓名")
    engName       = models.CharField(max_length=100,  verbose_name="英文名")
    ID_Card       = models.CharField(max_length=100,  verbose_name="身分證字號")
    dateOfBirth   = models.DateField(verbose_name="出生日期")
    # age         = models.IntegerField(max_length=100,  verbose_name="年齡")
    gender        = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name="性別")
    maritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT, verbose_name="婚姻狀態")
    highestEduLev = models.ForeignKey(EducationLevel, on_delete=models.PROTECT, verbose_name="最高教育程度")
    OTJStatus           = models.ForeignKey(
                            EmploymentStatus,
                            on_delete=models.PROTECT,
                            verbose_name="在職狀態"
                        )
    jobNum              = models.CharField(max_length=4, unique=True, verbose_name="工號")
    employeeAccount     = models.CharField(max_length=50, unique=True, verbose_name="員工帳號")
    department          = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="部門")
    jobTitle            = models.CharField(max_length=50, verbose_name="職稱")
    immediateSupervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="直屬主管")
    grade               = models.CharField(max_length=50, verbose_name="職等")
    empCategory         = models.ForeignKey(EmploymentCategory, on_delete=models.PROTECT, verbose_name="聘僱類別")
    recruitmentSource   = models.ForeignKey(RecruitmentSource, on_delete=models.PROTECT, verbose_name="招聘來源")
    companyPhone        = models.CharField(max_length=50, verbose_name="公司電話")
    extension           = models.CharField(max_length=50, verbose_name="分機")
    companyMobilePhone  = models.CharField(max_length=50, verbose_name="公司手機")
    companyMailbox      = models.CharField(max_length=50, verbose_name="公司信箱")
    startDate           = models.DateField(max_length=50, verbose_name="到職日期")
    resignationDate     = models.DateField(max_length=50, null=True, blank=True, verbose_name="離職日期")
    remark              = models.TextField  (max_length=50, verbose_name="備註")
    
    # 年齡計算
    def get_age(self):
        today = timezone.now().date()
        return relativedelta(today, self.dateOfBirth).years
    
    @property
    def age(self):
        return self.get_age()

    age.fget.short_description = '年齡'

    # 針對工號 帳號 資料編號的程式特殊修改
    def save(self, *args, **kwargs):
      if not self.jobNum:
          try:
              last_employee = Employee.objects.order_by('-jobNum').first()
              if last_employee:
                  last_num = int(last_employee.jobNum[1:])
                  self.jobNum = f'R{str(last_num + 1).zfill(3)}'
              else:
                  self.jobNum = 'R001'
          except Exception as e:
              print(f"Error generating jobNum: {e}")
              self.jobNum = 'R001'  # 設置默認值

      if not self.dataNum:
          try:
              last_instance = Employee.objects.order_by('dataNum').last()
              if last_instance:
                  last_number = int(last_instance.dataNum[2:])
                  self.dataNum = f'E-{str(last_number + 1).zfill(5)}'
              else:
                  self.dataNum = 'E-00001'
          except Exception as e:
              print(f"Error generating dataNum: {e}")
              self.dataNum = 'E-00001'  # 設置默認值
              
      super(Employee, self).save(*args, **kwargs)

    # 
    def __str__(self):
        return self.name
    # def __str__(self):
    #     return f"{self.jobNum} ({self.name})" # 假設你有一個 name 字段

    class Meta:
        verbose_name = "員工資料"
        verbose_name_plural = "員工資料"
        
# 針對寄發文件
class SendEmail(models.Model):
  subject = models.CharField(max_length=200, verbose_name='主題')
  message = models.TextField(verbose_name='留言訊息')
  from_email = models.EmailField(verbose_name='(從)來自郵件', default='georgiawang5332@gmail.com', editable=False)  # 設置為不可編輯    
  to_email = models.EmailField(verbose_name='(到)收件者郵件帳號')
  # 添加其他您需要的字段

  def __str__(self):
    return self.subject
  
  class Meta:
    verbose_name = "寄發郵件"
    verbose_name_plural = "寄發郵件"

# 加入群組
class GroupEmail(models.Model):
    number = models.AutoField(primary_key=True)  # 自動遞增的編號
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='group_emails')  # 關聯到 Employee 模型
    action = models.CharField(max_length=50, default='加入')  # 操作，預設為"加入"
    is_read = models.BooleanField(default=False) 
    added_at = models.DateTimeField(auto_now_add=True) #可以刪除

    def __str__(self):
        return f"Group Email {self.number}"

    class Meta:
        ordering = ['-number']  # 按編號排序
        unique_together = ['employee']  # 確保每個員工只能被添加一次
        # db_table = "employee"
        verbose_name = "群組郵件"
        verbose_name_plural = "群組郵件"

    @property
    def email(self):
        return self.employee.companyMailbox
    
# 3. 處理接收到的郵件：
class Email(models.Model):
    uid = models.CharField(max_length=255, unique=True, null=True)  # 添加 uid 字段
    subject = models.CharField(max_length=200, verbose_name='主題')
    message = models.TextField(verbose_name='留言訊息')
    from_email = models.EmailField(verbose_name='來自郵件')
    to_email = models.EmailField(verbose_name='收件者郵件帳號')
    received_at = models.DateTimeField(null=True, blank=True, verbose_name='接收時間')
    is_sent = models.BooleanField(default=False, verbose_name='是否已發送')
    folder = models.CharField(max_length=50, verbose_name='資料夾') # 新增的 folder 欄位
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  # 新增的 created_at 字段

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = '郵件'
        verbose_name_plural = '郵件'