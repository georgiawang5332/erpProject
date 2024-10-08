from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 設置 Django 項目的默認設置模組# 設定 Django 設定模組環境變數
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpProject.settings')

# 創建 Celery 實例# 創建 Celery 應用實例
app = Celery('erpProject')

# 從 Django 設置中加載配置# 從 Django 設定檔中載入設定
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現任務模組# 自動尋找並載入所有已註冊 Django 應用程式中的 tasks
app.autodiscover_tasks()

# 設置 Celery beat 調度任務
from celery.schedules import crontab

app.conf.beat_schedule = {
    'fetch-emails-every-10-minutes': {
        'task': 'your_project_name.tasks.fetch_emails_task',
        'schedule': crontab(minute='*/10'),
    },
}

# 使 Celery 支援 Django 的模型
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    # print('Request: {0!r}'.format(self.request))
    print(f'Request: {self.request!r}')
# 
app.conf.update(
    broker_connection_retry_on_startup=True,
)