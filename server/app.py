from flask import Flask, Response
import cv2

app = Flask(__name__)

# Ruta para el stream de video
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    camera = cv2.VideoCapture(0)  # Cambiar a 0 para usar la cámara por defecto
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Aquí es donde pasarías el frame al modelo de CV para procesamiento
            # Por ahora, solo convertiremos el frame a JPEG y lo enviaremos al cliente
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
