from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from apiclient import errors
import base64
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

BODY = '''
Dear {0},

Thank you for participating in the Kringle Draft 2018.
You are the Secret Santa for: {1}

Whether they have been naughty or nice the rules are the same:
- Find a gift just for them for $50 or less
- Wrap your gift and label with their name - but don’t reveal who you are
- Bring gift for exchange on Christmas Day
- Remember it’s a secret!

Merry Christmas,
The Kringle Draft Commissioner

'''


def send_mail(to, target):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    message = MIMEText(BODY.format(to.split(' ')[0],target.split(' ')[0].upper()))
    message['to'] = to.split(' ')[1]
    message['from'] = 'KringleDraft <oconnoat@gmail.com>'
    message['subject'] = 'Batch 3 [{},{}] KringleDraft 2018 DO NOT REPLY'.format(to.split(' ')[0],target.split(' ')[0].upper())

    msg_enc = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}


    try:
        message = (service.users().messages().send(userId='me', body=msg_enc).execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    draft = json.load(open('result.json','r'))
    for d in draft:
        send_mail(*d)
