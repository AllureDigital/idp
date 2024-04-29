
'''
from allauth.socialaccount.models import SocialToken
import requests

def fetch_emails(request):
    user = request.user
    social_token = SocialToken.objects.get(account__user=user, account__provider='google')
    access_token = social_token.token
    headers = {'Authorization': f'Bearer {access_token}'}
    # Query parameter to filter emails by label "inbox"
    params = {'q': 'label:inbox'}
    response = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages', headers=headers,params=params)
    email_messages = response.json().get('messages', [])

    detailed_emails = []
    for message in email_messages:
        message_id = message['id']
        message_response = requests.get(f'https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}', headers=headers)
        message_data = message_response.json()
        email_details = {'id': message_id}
        for header in message_data['payload']['headers']:
            if header['name'] in ['From', 'To', 'Subject']:
                email_details[header['name']] = header['value']
        detailed_emails.append(email_details)

    return detailed_emails
'''

'''
def fetch_emails(request):
    user = request.user
    social_token = SocialToken.objects.get(account__user=user, account__provider='google')
    access_token = social_token.token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages', headers=headers)
    emails = response.json()
    return emails



def fetch_emails(request):
    user = request.user
    social_token = SocialToken.objects.get(account__user=user, account__provider='google')
    access_token = social_token.token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages', headers=headers)
    emails = response.json().get('messages', [])
    
    detailed_emails = []
    for email in emails:
        email_id = email['id']
        email_response = requests.get(f'https://www.googleapis.com/gmail/v1/users/me/messages/{email_id}', headers=headers)
        detailed_email = email_response.json()
        detailed_emails.append(detailed_email)
    
    return detailed_emails

    '''


import requests
import base64
from allauth.socialaccount.models import SocialToken



def fetch_emails(request):
    user = request.user
    social_token = SocialToken.objects.get(account__user=user, account__provider='google')
    access_token = social_token.token
    headers = {'Authorization': f'Bearer {access_token}'}
    # Query parameter to filter emails by label "inbox"
    params = {'q': 'label:inbox'}
    response = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages', headers=headers, params=params)
    email_messages = response.json().get('messages', [])

    detailed_emails = []
    for message in email_messages:
        message_id = message['id']
        message_response = requests.get(f'https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}', headers=headers)
        message_data = message_response.json()

        # Initialize email_details with an empty body
        email_details = {'id': message_id, 'body': ''}

        payload = message_data.get('payload', {})
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    # Decode and store the email body
                    email_details['body'] = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
                elif part.get('mimeType') == 'text/html':
                    # For HTML emails, you might want to handle differently or in addition to text/plain
                    pass
        elif 'body' in payload:
            email_details['body'] = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        for header in payload.get('headers', []):
            if header['name'] in ['From', 'To', 'Subject']:
                email_details[header['name']] = header['value']

        detailed_emails.append(email_details)

    return detailed_emails
