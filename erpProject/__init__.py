from __future__ import absolute_import, unicode_literals
# 載入 celery 應用
from .celery import app as celery_app

# 明確指出這個模組應該被載入
__all__ = ('celery_app',)
