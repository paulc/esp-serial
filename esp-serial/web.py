
from microdot import Microdot, Response, redirect, send_file
import gc

app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="/static/normalize.css">
        <link rel="stylesheet" href="/static/skeleton.css">
        <script src="/static/htmx.min.js"></script>
        <title>ESP8266 Example Page</title>
    </head>
    <body>
        <div>
            <h1>ESP8266 Example Page</h1>
            <p>Hello from ESP8266!</p>
            <button hx-get="/square/99">Button</button>
        </div>
    </body>
</html>
'''


@app.route('', methods=['GET', 'POST'])
def root(request):
    print(request.headers)
    return Response(body=htmldoc, headers={'Content-Type': 'text/html'})

@app.route('/square/<int:n>', methods=['GET'])
def square(request,n):
    print(request.headers)
    print('n:',n)
    return Response(body='Square: {} = {}'.format(n,n*n), headers={'Content-Type': 'text/plain'})

@app.route('/static/<name>', methods=['GET'])
def static(request,name):
    try:
        content_type = Response.types_map.get(name.split('.')[-1],'application/octet-stream')
        response = send_file('/static/{}.gz'.format(name),content_type=content_type)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Cache-Control'] = 'max-age=86400'
    except OSError:
        try:
            response = send_file('/static/{}'.format(name))
            response.headers['Cache-Control'] = 'max-age=86400'
        except OSError:
            response = Response(body='Not Found\n',status_code=404)
    return response

while True:
    try:
        gc.collect()
        app.run(debug=True)
    except OSError as e:
        if e.args[0] in [104,]: # ECONNRESET
            pass
        else:
            raise

