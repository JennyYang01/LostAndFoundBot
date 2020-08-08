from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'TEST_ACCESS_TOKEN'
VERIFY_TOKEN = 'TEST_VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    """ Endpoint used for receiving messages from FB chat """
    # GET request is sent for FB to check the bot's verify token
    if request.method == 'GET':
        # verify token confirms that the requeest the bot received came from FB/Messenger
        token_sent = request.args.get('hub.verify_token')
        return verify_fb_token(token_sent)
    # POST request is sent when user sends us something, so we send a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # get Messenger ID of sender
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return 'Message Processed'


def verify_fb_token(token_sent):
    """ take token sent by facebook and verify it matches the verify token you sent """
    if token_sent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'


def get_message():
    """ gets the message to send back to the user """
    return 'Test response message'


def send_message(recipient_id, response):
    """ Sends the message using PyMessenger """
    bot.send_text_message(recipient_id, response)
    return 'success'


if __name__ == '__main__':
    app.run()
