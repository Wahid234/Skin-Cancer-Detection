
from flask import Flask, request, render_template
from PIL import Image
import numpy as np
import skin_cancer_detection as SCD
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def runhome():
    return render_template("home.html")


@app.route("/showresult", methods=["POST"])
def show():
    # Save the uploaded image
    pic = request.files["pic"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], pic.filename)
    pic.save(filepath)

    # Process the image
    inputimg = Image.open(filepath)
    inputimg = inputimg.resize((28, 28))
    img = np.array(inputimg).reshape(-1, 28, 28, 3)
    result = SCD.model.predict(img)

    # Interpret the result
    result = result.tolist()
    max_prob = max(result[0])
    class_ind = result[0].index(max_prob)
    diagnosis = "Skin Cancer Detected" if class_ind in range(7) else "No Skin Cancer Detected"
    cancer_type = SCD.classes[class_ind] if diagnosis == "Skin Cancer Detected" else "N/A"

    # Description based on the type of skin cancer
    descriptions = [
        "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion.",
        "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells — a type of cell within the skin that produces new skin cells as old ones die off.Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck",
        "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL)1",
        "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years. They are firm and often feel like a stone under the skin. ",
        "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with ‘melanocytic nevus’, but there are also sources that equate the term mole with any nevus form.",
        "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum.",
        "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."
    ]
    description = descriptions[class_ind] if diagnosis == "Skin Cancer Detected" else "N/A"

    return render_template(
        "reults.html",
        image_path=filepath,
        diagnosis=diagnosis,
        cancer_type=cancer_type,
        description=description,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
