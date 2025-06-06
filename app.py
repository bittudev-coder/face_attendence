from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import os
import datetime

app = Flask(__name__)  # Fixed: __name__
CORS(app)

# Folder jahan pe registered employee face images honge
KNOWN_FACES_DIR = os.path.join(os.path.dirname(__file__), "known_faces")  # Fixed: __file__

# Attendance log file path
ATTENDANCE_LOG = os.path.join(os.path.dirname(__file__), "attendance.csv")  # Fixed: __file__

# Load known face encodings aur employee IDs (filenames se)
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
                emp_id = os.path.splitext(filename)[0]  # filename without extension
                employee_ids.append(emp_id)
    return encodings, employee_ids

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image provided'}), 400

    file = request.files['image']
    temp_path = os.path.join(os.path.dirname(__file__), "temp.jpg")  # Fixed: __file__
    file.save(temp_path)

    unknown_image = face_recognition.load_image_file(temp_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_encodings:
        return jsonify({'status': 'failed', 'message': 'No face detected'}), 200

    known_encodings, employee_ids = load_known_faces()
    matches = face_recognition.compare_faces(known_encodings, unknown_encodings[0], tolerance=0.5)

    for idx, match in enumerate(matches):
        if match:
            emp_id = employee_ids[idx]
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Attendance log me entry karo
            with open(ATTENDANCE_LOG, "a") as f:
                f.write(f"{now},{emp_id}\n")
            return jsonify({'status': 'success', 'employee_id': emp_id}), 200

    return jsonify({'status': 'failed', 'message': 'No matching face found'}), 200

if __name__ == "__main__":  # Fixed: __name__
    os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
    print(f"Known faces dir: {KNOWN_FACES_DIR}")
    print(f"Attendance log path: {ATTENDANCE_LOG}")
    app.run(host='0.0.0.0', port=5000, debug=True)
