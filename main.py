from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/product_info', methods=['GET'])
def product_info():
    data = request.args

    ingredients = data['ingredients']

    response = get_product_info(ingredients=ingredients)

    return jsonify(response)


@app.route('/claim_check', methods=['GET'])
def claim_check():
    data = request.args

    ingredients = data['ingredients']
    claim = data['claim']

    response = check_claim(ingredients=ingredients,claim=claim)

    return jsonify(response)


@app.route('/diet_compliance', methods=['GET'])
def diet_compliance():
    data = request.args

    ingredients = data['ingredients']
    diet = data['diet']

    response = check_diet_compliance(ingredients=ingredients,diet=diet)

    return jsonify(response)


@app.route('/extract_ingredients', methods=['POST'])
def extract_ingredients():
    # Check if the request has a file part
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    
    # Save the file securely
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)
    
    extracted_ingredients = get_ingredients(filepath)
    
    os.remove(filepath)
    
    return jsonify({"ingredients": extracted_ingredients}), 200


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
