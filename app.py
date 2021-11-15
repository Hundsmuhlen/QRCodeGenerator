from flask import Flask, send_file, request, send_from_directory, render_template, url_for, make_response
import qrcode
import os


app = Flask(__name__, static_folder='static')


@app.route('/')
def hello_world():
    return render_template("input.html")

@app.route('/qr', methods=["POST"])
def showQR():
    data = request.form.get("data", "")
    print(f"DATA = {data}")

    image_file = makeQR(data)
    #Todo: Download funktion. Irgendwo muss gespeichert werden, was der Nutzer eigegeben hat, sonst lädt er das falsche Bild herunter
    resp = make_response(render_template("input.html", image_file=image_file))
    resp.set_cookie("URL", data)

    return resp
    #return send_file(as_attachment=True, path_or_file=path)
    #return send_file(img, as_attachment=True, mimetype="image/png", download_name="yourQRCode.png")

@app.route("/downloadqr", methods=["POST"])
def downloadQR():
    data = request.cookies.get("URL")
    image_file = makeQR(data)
    return send_file(as_attachment=True, path_or_file=image_file)

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
    return image_file

if __name__ == '__main__':
    app.run()
