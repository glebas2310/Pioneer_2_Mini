import cv2
import numpy as np

from pioneer_rknn import ModelContainer as mc
from pioneer_sdk2 import Camera, CameraType, ImageViewer

IMG_SIZE = (640, 640)
CONF_THRESHOLD = 0.45
NMS_THRESHOLD = 0.45
classNames = ['Give Way', 'No Entry', 'Pedestrian Crossing', 'Road Works', 'Speed Bump', 'parking', 'stop']

cam_main = Camera(camera_type=CameraType.MAIN)
viewer = ImageViewer()

def nms_numpy(boxes, scores, iou_thresh):
    if len(boxes) == 0: return []
    boxes = np.array(boxes)
    x1, y1 = boxes[:, 0], boxes[:, 1]
    x2, y2 = boxes[:, 0] + boxes[:, 2], boxes[:, 1] + boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = np.argsort(scores)[::-1]
    keep = []
    
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= iou_thresh)[0]
        order = order[inds + 1]
        
    return keep

def postprocess_yolo11(outputs, orig_shape):
    output = outputs[0]
    if output.ndim == 3: output = output[0]
    if output.shape[0] < output.shape[1]: output = output.T

    orig_h, orig_w = orig_shape
    x_scale = orig_w / IMG_SIZE[0]
    y_scale = orig_h / IMG_SIZE[1]

    boxes = output[:, :4]
    scores = output[:, 4:]
    class_ids = np.argmax(scores, axis=1)
    confidences = np.max(scores, axis=1)

    mask = confidences >= CONF_THRESHOLD
    boxes = boxes[mask]
    confidences = confidences[mask]
    class_ids = class_ids[mask]

    if len(boxes) == 0: return []

    cv_boxes = []
    for box in boxes:
        cx, cy, w, h = box
        cv_boxes.append([int((cx - w/2)*x_scale), int((cy - h/2)*y_scale), int(w*x_scale), int(h*y_scale)])

    indices = nms_numpy(cv_boxes, confidences, NMS_THRESHOLD)
    
    detections = []
    for idx in indices:
        detections.append({'box': cv_boxes[idx], 'conf': float(confidences[idx]), 'class_id': int(class_ids[idx])})
    return detections

def draw_detections(frame, detections):
    for det in detections:
        x, y, w, h = det['box']
        label = f"{classNames[det['class_id']]}: {det['conf']:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, max(y - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame

if __name__ == '__main__':
    MODEL_PATH = '/home/pioneermini/workspace/best_model.rknn'
    model = mc(MODEL_PATH, None, None)
    
    print("\nЗапуск нейросети...")
    print("Откройте в браузере: http://10.42.0.1:8889/stream")
    
    try:
        while True:
            frame = cam_main.get_cv_frame()
            if frame is None:
                continue
            
            orig_shape = frame.shape[:2]
            img_resized = cv2.resize(frame, IMG_SIZE)
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            input_tensor = np.expand_dims(img_rgb, 0)
            
            outputs = model.run([input_tensor])
            
            if outputs is not None:
                detections = postprocess_yolo11(outputs, orig_shape)
                frame = draw_detections(frame, detections)
            
            viewer.imshow(name='stream', frame=frame, fps=30)
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
        model.release()
