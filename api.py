from io import BytesIO

from werkzeug.wsgi import FileWrapper
from flask import Flask, request, send_file, Response

from listok import LaTeXProcessor


app = Flask(__name__)
processor = LaTeXProcessor()

@app.route('/', methods=['GET', 'POST'])
def main():
    problems = request.json
    bs = processor(problems)
    b = BytesIO(bs)
    w = FileWrapper(b)
    return Response(w, mimetype="application/pdf", direct_passthrough=True)
    # return send_file('main.pdf')

if __name__ == '__main__':
    app.run(debug=False, port=5002, host='0.0.0.0')