import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
import random
import requests
from tensorflow.keras.preprocessing.image import img_to_array
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = tf.keras.models.load_model("rps.h5")
CLASSES = ["paper", "rock", "scissors"]


def preprocess_image(base64_str):
       
    # Separa el header y la cadena codificada en base64
    _, encoded = base64_str.split(",", 1)
    # Decodifica la cadena en base64 en bytes
    decoded = base64.b64decode(encoded)
    # Convierte los bytes en una imagen PIL
    img = Image.open(BytesIO(decoded)).convert("RGB")
    # Redimensiona la imagen a 150x150 píxeles
    img = img.resize((150, 150))
    # Convierte la imagen a un arreglo numpy y normaliza los valores de píxeles
    img_array = img_to_array(img) / 255.0
    # Expande las dimensiones del arreglo para que sea compatible con el modelo
    return np.expand_dims(img_array, axis=0)


def decide_winner(user, computer):
    # Decide el ganador del juego según las reglas de piedra, papel o tijera.

    if user == computer:
        return "Draw"
    if (
        (user == "rock" and computer == "scissors")
        or (user == "paper" and computer == "rock")
        or (user == "scissors" and computer == "paper")
    ):
        return "You win!"
    else:
        return "Computer wins!"


@app.route("/")
def index():
    # Renderiza la página principal del juego.
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    # Obtiene los datos de la solicitud
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos en la solicitud"}), 400

    # Obtiene la imagen del gesto del usuario
    image_data = data.get("image")
    if not image_data:
        return jsonify({"error": "No se recibió la imagen en la solicitud"}), 400

    # Preprocesa la imagen como una entrada del modelo
    image = preprocess_image(image_data)
    # Realiza la predicción utilizando el modelo
    prediction = model.predict(image)
    # Determina el movimiento del usuario con la mayor probabilidad
    user_move = CLASSES[np.argmax(prediction)]
    # Genera un movimiento aleatorio para la mano
    computer_move = random.choice(CLASSES)
    # Computa el ganador
    result = decide_winner(user_move, computer_move)

    # Devuelve elmovimiento del usuario, el movimiento de la mano y el ganador
    return jsonify(
        {"user_move": user_move, "computer_move": computer_move, "result": result}
    )


@app.route("/move", methods=["POST"])
def move():
    # Obtiene los datos de la solicitud
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos en la solicitud"}), 400

    # Obtiene el movimiento deseado
    computer_move = data.get("computer_move")
    if not computer_move:
        return jsonify({"error": "No se especificó el movimiento"}), 400

    # Realiza el movimiento deseado de la mano desde el servidor de la misma
    try:
        response = requests.post(
            "http://192.168.149.1:5999/move",
            json={"computer_move": computer_move},
        )
        response_data = response.json()

        if response.status_code != 200:
            return jsonify({"error": response_data.get("error")}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"move": computer_move})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5997)
