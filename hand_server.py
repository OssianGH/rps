from LeArm import initLeArm, runActionGroup
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)
camera = cv2.VideoCapture(0)
ACTION_GROUPS = {
    "rock": "22_rock",
    "scissors": "23_scissors",
    "paper": "24_paper",
}
initLeArm([0, 0, 0, 0, 0, 0])


def generate_frames():
    while True:
        # Lee el frame de la cámara
        success, frame = camera.read()

        if not success:
            # Si no se lee, finaliza el bucle
            break
        else:
            # Rota el frame 180 grados
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            # Codifica el frame en un buffer JPEG
            _, buffer = cv2.imencode(".jpg", frame)
            # Convierte el buffer a bytes
            frame = buffer.tobytes()

            # Genera el frame para la transmisión
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def perform_arm_move(move_name):
    # Obtiene el action group según el nombre del movimiento
    action_group = ACTION_GROUPS.get(move_name)

    if not action_group:
        # Si no se encuentra, lanza una excepción
        raise Exception("Nombre de movimiento inválido")

    # Ejecuta el action group
    runActionGroup(action_group, 1)


@app.route("/")
def index():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/move", methods=["POST"])
def move():
    # Obtiene los datos de la solicitud
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos en la solicitud"}), 400

    # Obtiene el nombre del movimiento
    computer_move = data.get("computer_move")
    if not computer_move:
        return (jsonify({"error": "No se especificó el movimiento"}), 400)

    try:
        # Realiza el movimiento del brazo
        perform_arm_move(computer_move)

    except Exception as e:
        # Si ocurre un error, devuelve su mensaje
        return jsonify({"error": str(e)}), 400

    # Devuelve una respuesta exitosa
    return jsonify({"message": f"Performed move: {computer_move}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5999)
