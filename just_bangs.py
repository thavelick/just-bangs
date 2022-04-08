#!/usr/bin/python3
from urllib.parse import quote_plus, unquote_plus
import json
import http.server
import socketserver

with open('bang.js', 'r') as f:
    bangs = json.loads(f.read())

PORT = 8484
USAGE = (
    'give me a bang! Example: http://localhost:{}/gh!+just+bangs'
).format(PORT)

class JustBangsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = unquote_plus(self.path.lstrip('/'))
        bang = None 
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
            bang = bang.strip('!')
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

