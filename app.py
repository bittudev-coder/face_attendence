from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import os
import datetime

app = Flask(__name__)
CORS(app)

# Directories and paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "known_faces")
ATTENDANCE_LOG = os.path.join(BASE_DIR, "attendance.csv")
TEMP_IMAGE_PATH = os.path.join(BASE_DIR, "temp.jpg")

# Load known face encodings and employee IDs from images
def load_known_faces():
    encodings = []
    employee_ids = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            face_encs = face_recognition.face_encodings(image)
            if face_encs:
                encodings.append(face_encs[0])
                emp_id = os.path.splitext(filename)[0]
                employee_ids.append(emp_id)
    return encodings, employee_ids

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image provided'}), 400

    file = request.files['image']
    file.save(TEMP_IMAGE_PATH)

    unknown_image = face_recognition.load_image_file(TEMP_IMAGE_PATH)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_encodings:
        return jsonify({'status': 'failed', 'message': 'No face detected'}), 200

    known_encodings, employee_ids = load_known_faces()
    matches = face_recognition.compare_faces(known_encodings, unknown_encodings[0], tolerance=0.5)

    for idx, match in enumerate(matches):
        if match:
            emp_id = employee_ids[idx]
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(ATTENDANCE_LOG, "a") as f:
                f.write(f"{now},{emp_id}\n")
            return jsonify({'status': 'success', 'employee_id': emp_id}), 200

    return jsonify({'status': 'failed', 'message': 'No matching face found'}), 200

if __name__ == "__main__":
    # Ensure known_faces directory exists
    os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
    print(f"Known faces dir: {KNOWN_FACES_DIR}")
    print(f"Attendance log path: {ATTENDANCE_LOG}")

    # Use PORT from environment variable (important for Railway)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
