from flask import Flask
import numpy as np
from flask import Flask, render_template, request
from keras.models import load_model
from PIL import Image, ImageOps


app = Flask(__name__)

classes = {"0": "safe driving",
"1": "texting - right",
"2": "talking on the phone - right",
"3": "texting - left",
"4": "talking on the phone - left",
"5": "operating the radio",
"6": "drinking",
"7": "reaching behind",
"8": "hair and makeup",
"9": "talking to passenger"}

model = load_model("driver_model.h5")

def predict_label(img_path):
	test = Image.open(img_path)
	test = ImageOps.grayscale(test)
	test = test.resize((240, 240))
	test = np.array(test)
	test = test.reshape(-1, 240, 240, 1)
	prediction = model.predict(test)[0]
	label = np.argmax(prediction)
	return classes[str(label)]


@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction=p, img_path=img_path)

if __name__ == '__main__':
	# app.debug = True
	app.run(debug=True)
