import logging
import imaplib
import email
from email.header import decode_header
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from PersonnelAddressBook.models import Email

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch new emails from Gmail using IMAP'

    def handle(self, *args, **options):
        fetch_emails()

def fetch_emails():
    logger.info("開始獲取郵件")
    imap_server = "imap.gmail.com"
    email_address = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    with imaplib.IMAP4_SSL(imap_server) as imap:
        try:
            imap.login(email_address, password)
            logger.info("成功連接到 IMAP 服務器並登錄")
            
            folders_to_check = ["INBOX", "Spam", "[Gmail]/All Mail"]
            # folders_to_check = ["INBOX", "已發送郵件", "垃圾郵件", "[Gmail]/所有郵件"]
            for folder in folders_to_check:
                process_folder(imap, folder)
        except Exception as e:
            logger.error(f"獲取郵件時出錯: {str(e)}", exc_info=True)

def process_folder(imap, folder):
    logger.info(f"檢查文件夾: {folder}")
    status, folders = imap.list()

    if status == 'OK':
        # 確保 folder_name 被解碼為字符串
        if any(folder_name.decode().endswith(f' "{folder}"') for folder_name in folders):
            status, folder_info = imap.select(folder)
            if status != 'OK':
                logger.warning(f"無法選擇文件夾 {folder}: {folder_info}")
                return
        else:
            logger.warning(f"文件夾 {folder} 不存在")
            return
    else:
        logger.error("無法獲取文件夾列表")
        return

    last_email = Email.objects.filter(folder=folder).order_by('-uid').first()
    last_uid = last_email.uid if last_email else '0'
    status, messages = imap.uid('search', None, f'UID {int(last_uid) + 1}:*')
    # status, messages = imap.uid('search', None, 'ALL')

    if status == 'OK':
        for num in messages[0].split():
            try:
                process_email(imap, num, folder)
            except Exception as e:
                logger.error(f"處理郵件時出錯: {str(e)}", exc_info=True)
    else:
        logger.warning(f"在文件夾 {folder} 中搜索郵件失敗")

def process_email(imap, num, folder):
    status, msg_data = imap.uid('fetch', num, '(RFC822)')
    if status != 'OK':
        logger.warning(f"無法獲取郵件 UID: {num}")
        return

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_body = response_part[1]
            email_message = email.message_from_bytes(email_body)

            subject = decode_header_string(email_message["Subject"])
            logger.info(f"處理郵件: {subject}")

            sender = decode_header_string(email_message["From"])
            recipient = decode_header_string(email_message["To"])

            message = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        charset = part.get_content_charset() or 'utf-8'
                        message = part.get_payload(decode=True).decode(charset, errors='replace')
                        break
            else:
                charset = email_message.get_content_charset() or 'utf-8'
                message = email_message.get_payload(decode=True).decode(charset, errors='replace')

            uid = num.decode()
            if not Email.objects.filter(uid=uid).exists():
                received_at = email.utils.parsedate_to_datetime(email_message["Date"])
                if received_at.tzinfo is None:
                    received_at = timezone.make_aware(received_at)
                
                Email.objects.create(
                    uid=uid,
                    subject=subject,
                    message=message,
                    from_email=sender,
                    to_email=recipient,
                    received_at=received_at,
                    is_sent=False,
                    folder=folder
                )
                logger.info(f"成功保存郵件: {subject}")
            else:
                logger.info(f"郵件已存在，跳過: {subject}")

def decode_header_string(header):
    decoded_parts = decode_header(header)
    return ' '.join([
        part.decode(encoding or 'utf-8', errors='replace') if isinstance(part, bytes) else part
        for part, encoding in decoded_parts
    ])


# def process_email(imap, num, folder):
#     status, msg_data = imap.uid('fetch', num, '(RFC822)')
#     if status != 'OK':
#         logger.warning(f"無法獲取郵件 UID: {num}")
#         return

#     for response_part in msg_data:
#         if isinstance(response_part, tuple):
#             email_body = response_part[1]
#             email_message = email.message_from_bytes(email_body)

#             subject, encoding = decode_header(email_message["Subject"])[0]
#             if isinstance(subject, bytes):
#                 subject = subject.decode(encoding or 'utf-8', errors='replace')
#             logger.info(f"處理郵件: {subject}")

#             sender = email_message["From"]
#             recipient = email_message["To"]

#             if email_message.is_multipart():
#                 for part in email_message.walk():
#                     if part.get_content_type() == "text/plain":
#                         message = part.get_payload(decode=True).decode(errors='replace')
#                         break
#             else:
#                 message = email_message.get_payload(decode=True).decode(errors='replace')

#             uid = num.decode()
#             if not Email.objects.filter(uid=uid).exists():
#                 received_at = email.utils.parsedate_to_datetime(email_message["Date"])
#                 if received_at.tzinfo is None:
#                     received_at = timezone.make_aware(received_at)
                
#                 Email.objects.create(
#                     uid=uid,
#                     subject=subject,
#                     message=message,
#                     from_email=sender,
#                     to_email=recipient,
#                     received_at=received_at,
#                     is_sent=False,
#                     folder=folder
#                 )
#                 logger.info(f"成功保存郵件: {subject}")
#             else:
#                 logger.info(f"郵件已存在，跳過: {subject}")




