#!/usr/bin/python3
from pathlib import Path
from urllib.parse import quote_plus, unquote_plus
import json
import http.server
import os
import socketserver

DEFAULT_BANG = os.environ.get('JUST_BANGS_DEFAULT_BANG', None)
PORT = int(os.environ.get('JUST_BANGS_PORT', 8484))
MAIN_FILE = os.environ.get('JUST_BANGS_MAIN_FILE', 'bang.js')
CUSTOM_FILE = os.environ.get('JUST_BANGS_CUSTOM_FILE', 'custom-bang.js')
BASE_URL_PATH = '/' + os.environ.get('JUST_BANGS_BASE_URL_PATH', '').strip('/')

LOGO_FILE = 'just-bangs.svg'
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
        path = self.path

        # strip off the base path,
        if path.startswith(BASE_URL_PATH):
            path = '/' + path[len(BASE_URL_PATH):]

        # when constructing a url, the query can be specified after the first
        # slash like this:
        #  * http://localhost:8484/my+query+sp!
        # or, to support the search from the homepage, the query can be
        # specified in a querystring variable q like this:
        #  * http://localhost:8484/?q=my+query+sp!
        # In either case, the query can be in a subfolder, so everything
        # before the last slash in the url will be ignored
        query = unquote_plus( # url decode
            path # the path and querystring
            .split('/')[-1:][0] # get everything after the last /
            .split('?q=')[-1:][0] # if there's  querystirng variable `q`,
                                  # get the value of that
        )
        print(query)

        if len(query) == 0:
            self.do_file('index.html', 'text/html')
            return
        if query == LOGO_FILE:
            self.do_file(LOGO_FILE, 'image/svg+xml')
            return

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
                return

        self.do_text(USAGE)

    def do_file(self, path, content_type):
        with open(path, 'r') as f:
            content = f.read()
        self.do_text(content, content_type)

    def do_search(self, bang_info, query):
        url = bang_info.get('u')
        url = url.replace('{{{s}}}', quote_plus(query))
        self.do_redirect(url)

    def do_redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def do_text(self, text, content_type='text/plain'):
        text = str.encode(text)
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', len(text))
        self.end_headers()
        self.wfile.write(text)

with socketserver.TCPServer(("", PORT), JustBangsHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
