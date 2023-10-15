import os 
from twilio.rest import Client

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth = os.environ.get('TWILIO_AUTH_TOKEN')
whatsapp = os.environ.get('TWILIO_WHATSAPP')

cleint = Client(account_sid,auth)
def sendMessage (senderid,message):
    res = cleint.messages.create(
        body=message,
        from_=whatsapp,
        to= senderid
    )
    return res
def sendQr (senderid):
    res = cleint.messages.create(
        body='https://demo.twilio.com/owl.png',
        from_=whatsapp,
        to= senderid
    )
    return res