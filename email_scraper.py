from pathlib import Path
import email, getpass, imaplib, os

# your gmail imap settings have to be enabled for this script to work
EMAIL_PROVIDER  = "@gmail.com"
EMAIL_ADDR = os.environ.get("MAIL_USERNAME") + EMAIL_PROVIDER
EMAIL_PWD = os.environ.get("MAIL_PASSWORD")
TARGET_INBOX = "Daily Coding Problem"
DESTINATION_DIR = "/Users/Jeff/Dropbox/Coding/daily_coding_problem/"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

#login to email with provided email/pwd/target inbox
mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(EMAIL_ADDR, EMAIL_PWD)
mail.select('"%s"' % TARGET_INBOX)

#returns ids of all mail in the target inbox
type, data = mail.search(None, 'ALL')
mail_ids = data[0]

id_list = mail_ids.split()   
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

#If message is multi-part we only want the text version of the body, this fetches body.
for mail_id in range(first_email_id, latest_email_id+1):
    status, data = mail.fetch(str(mail_id), '(RFC822)')
    email_msg = email.message_from_bytes(data[0][1]) 
    if email_msg.is_multipart():
        for part in email_msg.walk():       
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True) 
                body = body.decode('utf-8')
                title = "problem" + str(mail_id) + ".py"
                save_dest = str(DESTINATION_DIR + title)
                
                #don't overwrite the file if this file already exists, try to save some time
                if Path(save_dest).exists():
                    break

                myfile = open(save_dest, 'w+')
                myfile.write("'''" + body + "'''")
                myfile.close()
                
            elif part.get_content_type() == "text/html":
                continue


            
