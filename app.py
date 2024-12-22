from flask import Flask, request, jsonify,render_template,send_file
from ultralytics import YOLO
from PIL import Image
import os
import cv2
import io


app = Flask(__name__)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # 'n' is for nano; change to 's', 'm', or 'l' for larger models

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')

def index():
    return  render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    img=cv2.imread(file_path)

    # Perform object detection
    results = model(img, conf=0.25)  # Adjust confidence threshold as needed



    # Parse results
    detections = []
    for box in results[0].boxes.data.tolist():  # YOLOv8 outputs bounding boxes
        x1, y1, x2, y2, confidence, class_id = box
        label = model.names[int(class_id)]  # Get the class label from the model
        detections.append({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'confidence': confidence,
            'class_id': int(class_id),
            'label': label
        })

        # Draw rectangle and label on the image
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, f"{label} {confidence:.2f}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the processed image
    processed_path = os.path.join(PROCESSED_FOLDER, f'processed_{file.filename}')
    cv2.imwrite(processed_path, img)


    #return jsonify({'detections': detections})

    return jsonify({
        'metadata': detections,
        'processed_image_url': f'/processed/{file.filename}'})

@app.route('/processed/<filename>', methods=['GET'])
def serve_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, f'processed_{filename}'), mimetype='image/jpeg')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
