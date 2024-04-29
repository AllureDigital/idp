# helpers.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialAccount
import base64
from email.mime.text import MIMEText

def get_gmail_service(user):
    social_account = SocialAccount.objects.get(user=user, provider='google')
    credentials = Credentials(token=social_account.socialtoken_set.get(account=social_account).token)
    return build('gmail', 'v1', credentials=credentials)


def create_message(to_email, cc_email, bcc_email, subject, body):
    message = MIMEText(body)
    message['to'] = to_email
    message['cc'] = cc_email
    message['bcc'] = bcc_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
