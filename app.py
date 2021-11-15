from flask import Flask, send_file, request, send_from_directory, render_template, url_for
import qrcode
import os


app = Flask(__name__, static_folder='static')


@app.route('/')
def hello_world():
    return render_template("input.html")

@app.route('/qr', methods=["POST"])
def makeQR():
    data = request.form.get("data", "")
    print(f"DATA = {data}")
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

    #path = f"/static/{name}"
    img.save(path)
    image_file = url_for('static', filename=name)
    print(image_file)

    return render_template("input.html", image_file=image_file)
    #return send_file(as_attachment=True, path_or_file=path)
    #return send_file(img, as_attachment=True, mimetype="image/png", download_name="yourQRCode.png")

if __name__ == '__main__':
    app.run()
