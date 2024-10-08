import imaplib
import email
from email.header import decode_header

def check_inbox():
    # 連接到 Gmail 伺服器
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    # 使用您的帳號和應用程式密碼登入
    mail.login("georgiawang5332@gmail.com", "spotksfpejpmbndp")

    # 選擇收件匣
    mail.select("inbox")

    # 搜索未讀郵件
    status, messages = mail.search(None, 'UNSEEN')
    
    # 轉化郵件ID為列表
    messages = messages[0].split()

    for mail_id in messages:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # 獲取郵件標題
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # 如果是bytes，則解碼
                    subject = subject.decode(encoding if encoding else "utf-8")
                # 獲取發件人
                from_ = msg.get("From")
                print("Subject:", subject)
                print("From:", from_)

                # 如果郵件是多部分的
                if msg.is_multipart():
                    for part in msg.walk():
                        # 如果是純文字部分
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print("Body:", body)
                else:
                    # 獲取郵件正文
                    body = msg.get_payload(decode=True).decode()
                    print("Body:", body)
