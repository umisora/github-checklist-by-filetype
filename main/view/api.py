from main import app

import os
import json
import re
from flask import jsonify, request
from main.lib.webhook import Webhook


@app.route('/webhook/github', methods=['POST'])
def webhook_github():
    # signature = request.headers.get('X-Hub-Signature')

    if not _verify_request_signature(request.args.get('token')):
        return "Signature is UnMatch.", 401

    print("********** Hello API *************")
    message = Webhook.run(
        request.headers.get('X-GitHub-Event'),
        request.get_data().decode('utf-8')
    )
    print(message, '200')
    return message, 200


def _verify_request_signature(signature):
    GITHUB_WEBHOOK_SECRET_TOKEN = os.getenv(
        'GITHUB_WEBHOOK_SECRET_TOKEN', "dummy")
    if signature != GITHUB_WEBHOOK_SECRET_TOKEN:
        print("Token is UnMatch")
        return False
    else:
        print("Token is Match")
        return True
