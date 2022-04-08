#!/usr/bin/python3
from pathlib import Path
from urllib.parse import quote_plus, unquote_plus
import json
import http.server
import os
import re
import socketserver

DEFAULT_BANG = os.environ.get('JUST_BANGS_DEFAULT_BANG', None)
PORT = int(os.environ.get('JUST_BANGS_PORT', 8484))
MAIN_FILE = os.environ.get('JUST_BANGS_MAIN_FILE', 'bang.js')
CUSTOM_FILE = os.environ.get('JUST_BANGS_CUSTOM_FILE', 'custom-bang.js')
USAGE = (
    'give me a bang! Example: http://localhost:{}/gh!+just+bangs'
).format(PORT)


with open(MAIN_FILE, 'r') as f:
    bangs = json.loads(f.read())

if Path(CUSTOM_FILE).exists():
    with open(CUSTOM_FILE, 'r') as f:
        bangs = json.loads(f.read()) + bangs

class JustBangsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = unquote_plus(re.sub(r'[^/]*/', '', self.path))
        bang = DEFAULT_BANG
        non_bangs = []

        # This is probably a little too naive. DDG doesn't treat words with
        # `!` which are inside quotes as bangs. But this will probably work
        # for 99% of cases for now.
        for word in query.split(' '):
            if word[:1] == '!':
                bang = word[1:]
            elif word[-1:] == '!':
                bang = word[:-1]
            else:
                non_bangs.append(word)

        if bang:
            bang = bang.strip('!').lower()
            matching_bang_info = [b for b in bangs if b.get('t') == bang]
            if len(matching_bang_info) > 0 and len(non_bangs) > 0:
                self.do_search(matching_bang_info[0], ' '.join(non_bangs))

        self.do_text(USAGE)

    def do_search(self, bang_info, query):
        url = bang_info.get('u')
        url = url.replace('{{{s}}}', quote_plus(query))
        text = json.dumps({
            'info': bang_info,
            'query': quote_plus(query),
            'url': url,
        })
        self.do_redirect(url)

    def do_redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def do_text(self, text):
        text = str.encode(text)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', len(text))
        self.end_headers()
        self.wfile.write(text)

with socketserver.TCPServer(("", PORT), JustBangsHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

