from django.db import models 

# Create your models here.
class SendEmail(models.Model):
  subject = models.CharField(max_length=200, verbose_name='主題')
  message = models.TextField(verbose_name='留言訊息')
  from_email = models.EmailField(verbose_name='來自郵件', default='georgiawang5332@gmail.com', editable=False)  # 設置為不可編輯    
  to_email = models.EmailField(verbose_name='員工郵件帳號')
  # 添加其他您需要的字段

  def __str__(self):
    return self.subject
  
  class Meta:
    verbose_name = "寄發郵件"
    verbose_name_plural = "寄發郵件"