from flask import Flask, request
from pymessenger.bot import Bot
import click
import sqlite3
from flask import g

DATABASE = 'lost_and_found.db'
app = Flask(__name__)
ACCESS_TOKEN = 'EAAEctZAzctfIBAOku9J0VXlk83nAysNxeDRRUD0aeUFY6NMiP859XhymgDprEs2sVC9sbZAHwF6gUjRZClfxc5kGeg7m8zXqsdmJL92kyFCzHQCzsKzA9rZCZBE9ytHZASLDv6DxQct0yP4TTEDkKDndcdV26Fpg46hnq4oxLNJgZDZD'
VERIFY_TOKEN = 'TEST_VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)


"""Messenger Bot portion:"""


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


"""Initialize DB:"""


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


"""Initialize DB command:"""
@app.cli.command("init-db")
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')


if __name__ == '__main__':
    app.run()
