from flask import Flask, send_file, request, send_from_directory, render_template
import qrcode
import os


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("input.html")

@app.route('/qr', methods=["POST"])
def makeQR():
    data = request.args.get("data", "")
    img = qrcode.make(data)
    path = os.path.join(os.getcwd(), "qrcode.png")
    print(path)
    img.save(path)
    return send_file(as_attachment=True, path_or_file=path)
    #return send_file(img, as_attachment=True, mimetype="image/png", download_name="yourQRCode.png")

if __name__ == '__main__':
    app.run()
