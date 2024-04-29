from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from django.shortcuts import render
from django.http import HttpResponse
import os
import pickle

from django.shortcuts import render,redirect
from .utils import fetch_emails
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .forms import EmailForm
from .helpers import get_gmail_service, create_message, send_email
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, redirect
from .forms import EmailForm
from allauth.socialaccount.models import SocialAccount
from .helpers import get_gmail_service, create_message, send_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReplyEmailForm
from .helpers import get_gmail_service, create_message, send_email
from allauth.socialaccount.models import SocialAccount


@login_required
def email_list(request):
    emails = fetch_emails(request)
    print(emails)
    return render(request, 'ems/list_emails.html', {'emails': emails})

@login_required
def email_detail(request, email_id):
    # Fetch email details using your existing function
    emails = fetch_emails(request)
    
    # Find the email with the provided ID
    for email in emails:
        if email['id'] == email_id:
            return render(request, 'ems/email_detail.html', {'email': email})
    
    # If email with the provided ID is not found, return a 404 error
    return render(request, '404.html')

def compose_email(request):
    # Initialize form without any initial values
    form = EmailForm(request.POST or None)

    # Check if user is authenticated
    if request.user.is_authenticated:
        # Check if user has a Google social account
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Get user's email from Google social account
            user_email = social_account.extra_data.get('email')
            # Update form's "from_email" field with the user's email as the initial value
            form.fields['from_email'].initial = user_email

    if request.method == 'POST':
        if form.is_valid():
            # Get user's Gmail service
            service = get_gmail_service(request.user)
            
            # Get email details from the form
            to_email = form.cleaned_data['to_email']
            cc_email = form.cleaned_data['cc_email']
            bcc_email = form.cleaned_data['bcc_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            # Print email details for debugging
            print(f"To: {to_email}")
            print(f"CC: {cc_email}")
            print(f"BCC: {bcc_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")

            # Create email message
            message = create_message(to_email, cc_email, bcc_email, subject, body)

            # Send email (assuming send_email function is called here)
            send_email(service, 'me', message)

            # Redirect or show success message
            #return redirect('email_list')
            return redirect('sent_email')

    return render(request, 'ems/compose_email.html', {'form': form, 'user_email': user_email})

def sent_email(request):
    # This view can be used for handling the actual sending of the email if needed
    return render(request, 'ems/email_sent.html')


def reply_email(request, email_id):
    # Fetch the original email details
    emails = fetch_emails(request)
    original_email = None
    for email in emails:
        if email['id'] == email_id:
            original_email = email
            break
    if original_email is None:
        messages.error(request, 'Email not found.')
        return redirect('email_list')
    
    # Print the original_email dictionary to inspect its structure
    #print(original_email)

   
    # Prepare the subject for the reply
    subject = original_email['Subject']
    if not subject.startswith("Re:"):
        subject = f"Re: {subject}"
    # Pre-fill the reply form with appropriate values
    form = ReplyEmailForm(initial={
        'from_email': request.user.email,
        'to_email': original_email['From'],
        'cc_email': original_email.get('CC', ''),
        'bcc_email': original_email.get('BCC', ''),
        'subject': subject,
        'body': f"\n\n\n-----Original Message-----\n{original_email['body']}"
    })
    
    if request.method == 'POST':
        form = ReplyEmailForm(request.POST)
        if form.is_valid():
            # Get user's Gmail service
            service = get_gmail_service(request.user)
            
            # Get email details from the form
            to_email = form.cleaned_data['to_email']
            cc_email = form.cleaned_data['cc_email']
            bcc_email = form.cleaned_data['bcc_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            # Create email message
            message = create_message(to_email, cc_email, bcc_email, subject, body)

            # Send email
            send_email(service, 'me', message)

            # Redirect or show success message
            messages.success(request, 'Email sent successfully!')
            return redirect('email_list')
        else:
            messages.error(request, 'Error sending email. Please check the form.')

    return render(request, 'ems/reply_email.html', {'form': form,'email_id': email_id})


'''
@login_required
def email_list(request):
    user_id = request.user.id
    cache_key = f'cached_emails_{user_id}'
    
    # Check if email data is cached for the current user
    emails = cache.get(cache_key)
    if not emails:
        # Fetch email details if not cached
        emails = fetch_emails(request)
        # Cache the fetched email data for 5 minutes (300 seconds)
        cache.set(cache_key, emails, timeout=1000)
    return render(request, 'ems/list_emails.html', {'emails': emails})

@login_required
def email_detail(request, email_id):
    user_id = request.user.id
    cache_key = f'cached_emails_{user_id}'
    
    # Check if email data is cached for the current user
    emails = cache.get(cache_key)
    if not emails:
        # Fetch email details if not cached
        emails = fetch_emails(request)
        # Cache the fetched email data for 5 minutes (300 seconds)
        cache.set(cache_key, emails, timeout=1000)
    
    # Find the email with the provided ID
    for email in emails:
        if email['id'] == email_id:
            return render(request, 'ems/email_detail.html', {'email': email})
    
    # If email with the provided ID is not found, return a 404 error
    return render(request, '404.html')
'''

'''
@login_required
def email_list(request):
    emails = fetch_emails(request)
    print(emails)
    return render(request, 'ems/list_emails.html', {'emails': emails})


@login_required
def email_detail(request, email_id):
    # Check if email data is cached
    emails = cache.get('cached_emails')
    if not emails:
        # Fetch email details if not cached
        emails = fetch_emails(request)
        # Cache the fetched email data for 5 minutes (300 seconds)
        cache.set('cached_emails', emails, timeout=300)
    
    # Find the email with the provided ID
    for email in emails:
        if email['id'] == email_id:
            return render(request, 'ems/email_detail.html', {'email': email})
    
    # If email with the provided ID is not found, return a 404 error
    return render(request, '404.html')
'''




'''
def compose_email(request):
    if request.user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            user_email = social_account.extra_data.get('email')
            form = EmailForm(request.POST or None, user_email=user_email)
        else:
            form = EmailForm(request.POST or None)
    else:
        form = EmailForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Get user's Gmail service
            service = get_gmail_service(request.user)
            
            # Get email details from the form
            to_email = form.cleaned_data['to_email']
            cc_email = form.cleaned_data['cc_email']
            bcc_email = form.cleaned_data['bcc_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            # Print email details for debugging
            print(f"To: {to_email}")
            print(f"CC: {cc_email}")
            print(f"BCC: {bcc_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")

            # Create email message
            message = create_message(to_email, cc_email, bcc_email, subject, body)

            # Send email (assuming send_email function is called here)
            send_email(service, 'me', message)

            # Redirect or show success message
            #return redirect('email_list')
            return redirect('sent_email')

    return render(request, 'ems/compose_email.html', {'form': form})
'''




'''
@login_required
def email_detail(request, email_id):
    email = Email.objects.get(id=email_id)
    return render(request, 'email_detail.html', {'email': email})

@login_required
def email_list(request):
    emails = fetch_emails(request)
    print(emails)
    return render(request, 'ems/list_emails.html', {'emails': emails})

@login_required
def email_detail(request, email_id):
    # Fetch email details using your existing function
    emails = fetch_emails(request)
    
    # Find the email with the provided ID
    for email in emails:
        if email['id'] == email_id:
            return render(request, 'ems/email_detail.html', {'email': email})
    
    # If email with the provided ID is not found, return a 404 error
    return render(request, '404.html')

@login_required
def email_list(request):
    # Check if email data is cached
    emails = cache.get('cached_emails')
    if not emails:
        # Fetch email details if not cached
        emails = fetch_emails(request)
        # Cache the fetched email data for 5 minutes (300 seconds)
        cache.set('cached_emails', emails, timeout=300)
    return render(request, 'ems/list_emails.html', {'emails': emails})

def email_detail(request, email_id):
    # Check if email data is cached
    emails = cache.get('cached_emails')
    if not emails:
        # Fetch email details if not cached
        emails = fetch_emails(request)
        # Cache the fetched email data for 5 minutes (300 seconds)
        cache.set('cached_emails', emails, timeout=300)
    
    # Find the email with the provided ID
    for email in emails:
        if email['id'] == email_id:
            return render(request, 'ems/email_detail.html', {'email': email})
    
    # If email with the provided ID is not found, return a 404 error
    return render(request, '404.html')


'''


'''
# Define global variables
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRET_FILE = ''
SERVICE_NAME = 'gmail'
USER_ID = 'me'

# Function to get Gmail service
def get_gmail_service():
    creds = None
    # Check if token.pickle file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If credentials are not valid or not available, authenticate user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Build and return the Gmail service
    service = build(SERVICE_NAME, 'v1', credentials=creds)
    return service

# Function to retrieve a list of emails from the user's inbox
def list_emails(request):
    service = get_gmail_service()
    results = service.users().messages().list(userId=USER_ID).execute()
    messages = results.get('messages', [])
    return render(request, 'list_emails.html', {'messages': messages})

# Function to fetch detailed information about a specific email
def get_email(request, email_id):
    service = get_gmail_service()
    message = service.users().messages().get(userId=USER_ID, id=email_id).execute()
    return render(request, 'email_detail.html', {'message': message})

# Function to compose and send new emails
def compose_email(request):
    if request.method == 'POST':
        service = get_gmail_service()
        message = MIMEText(request.POST['body'])
        message['to'] = request.POST['to']
        message['subject'] = request.POST['subject']
        raw_message = urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId=USER_ID, body={'raw': raw_message}).execute()
        return HttpResponse('Email sent successfully!')
    return render(request, 'compose_email.html')

# Function to reply to or forward existing emails
def reply_forward_email(request, email_id):
    if request.method == 'POST':
        service = get_gmail_service()
        message = service.users().messages().get(userId=USER_ID, id=email_id).execute()
        if request.POST['action'] == 'reply':
            reply = MIMEText(request.POST['body'])
            reply['to'] = message['payload']['headers'][0]['value']
            reply['subject'] = "Re: " + message['payload']['headers'][16]['value']
            raw_reply = urlsafe_b64encode(reply.as_bytes()).decode()
            service.users().messages().send(userId=USER_ID, body={'raw': raw_reply}).execute()
            return HttpResponse('Reply sent successfully!')
        elif request.POST['action'] == 'forward':
            forward = MIMEText(request.POST['body'])
            forward['to'] = request.POST['to']
            forward['subject'] = "Fwd: " + message['payload']['headers'][16]['value']
            raw_forward = urlsafe_b64encode(forward.as_bytes()).decode()
            service.users().messages().send(userId=USER_ID, body={'raw': raw_forward}).execute()
            return HttpResponse('Email forwarded successfully!')
    message = service.users().messages().get(userId=USER_ID, id=email_id).execute()
    return render(request, 'reply_forward_email.html', {'message': message})

# Your Django views for rendering templates and handling HTTP requests



'''
