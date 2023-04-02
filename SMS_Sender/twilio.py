from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = 'AC5c26da8824935273141dd1cd696d847c'
auth_token = 'd656e5ed3afa70c1d74923cfaf98294f'

# Create a new Twilio client object
client = Client(account_sid, auth_token)