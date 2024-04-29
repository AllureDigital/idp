

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
from django.contrib.auth.decorators import login_required

# Function to fetch detailed information about a specific email

""" def get_email(request, email_id):
    service = get_gmail_service()
    message = service.users().messages().get(userId=USER_ID, id=email_id).execute()
    return render(request, 'email_detail.html', {'message': message})

    # Define global variables
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRET_FILE = 'ems/client_secret.json'
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
def profile(request):
    service = get_gmail_service()
    results = service.users().messages().list(userId=USER_ID).execute()
    messages = results.get('messages', [])
    return render(request, 'dashboard/profile.html', {'messages': messages})"""


def profile(request):
    return render(request, 'dashboard/profile.html')


def index(request):
    return render(request, 'dashboard/index.html')