from flask import Flask, send_file, request, send_from_directory, render_template, url_for, make_response
import qrcode
import os


app = Flask(__name__, static_folder='static')


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/qr', methods=["GET", "POST"])
def showQR():
    if request.method == "GET":
        data = request.args.get("data", "")
    else:
        return render_template("index.html")

    image_file, name = makeQR(data)
    resp = make_response(render_template("image.html", image_file=image_file, data=data))
    resp.set_cookie("URL", data)

    return resp

@app.route("/downloadQR", methods=["GET", "POST"])
def downloadQR():
    data = request.form.get("data")
    image_file, name = makeQR(data)
    return send_from_directory(directory="static", path=name, as_attachment=True)

def makeQR(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    name = "qrcode.png"
    path = os.path.join(os.getcwd(), "static", name)

    img.save(path)
    image_file = url_for('static', filename=name)
    return image_file, name

if __name__ == '__main__':
    app.run()
