from uuid import uuid4
import cv2
import tensorflow as tf


class Classifier(object):
    def __init__(self, media_root):
        self.IMAGE_H = 416
        self.IMAGE_W = 416
        self.classes = self.load_labels('./tf_models/labels.txt')
        self.media_root = media_root
        self.ALLOWED_CLASSES = ['laptop', 'keyboard', 'person']

        with tf.gfile.FastGFile('./tf_models/ssd_mobilenet_v2_coco_2018_03_29.pb', 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        self.sess = tf.Session()
        self.sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        self.num_detections = self.sess.graph.get_tensor_by_name('num_detections:0')
        self.detection_scores = self.sess.graph.get_tensor_by_name('detection_scores:0')
        self.detection_boxes = self.sess.graph.get_tensor_by_name('detection_boxes:0')
        self.detection_classes = self.sess.graph.get_tensor_by_name('detection_classes:0')

        self.images_saved_to_disk = {'0123': ['img1.jpg', 'img2.jpg']}

    @staticmethod
    def load_labels(label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    @staticmethod
    def open_image_file_from_disk(image_path):
        img = cv2.imread(image_path)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return frame

    def classify_video(self, video_path, unique_id=None):
        vid = cv2.VideoCapture(video_path)
        while True:
            return_value, frame = vid.read()
            if return_value:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.classify_image(frame, unique_id)
            else:
                break

    def classify_image(self, image, unique_id=None):
        # Detect objects
        rows = image.shape[0]
        cols = image.shape[1]
        inp = cv2.resize(image, (300, 300))

        # Run the model
        out = self.sess.run([self.num_detections,
                             self.detection_scores,
                             self.detection_boxes,
                             self.detection_classes],
                            feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        num_detections = int(out[0][0])
        # images_saved_to_disk = []

        for obj in range(num_detections):
            class_id = int(out[3][0][obj])
            print('class_id:{}'.format(class_id))
            if self.classes[class_id] == 'person':
                print('Person detected')
                # Detect faces
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
                detected_faces = face_cascade.detectMultiScale(grayscale_image, 1.2, 6)
                if len(detected_faces) >= 1:
                    x, y, width, height = detected_faces[0]
                    self.write_to_disk(image, x, y, x+width, y+height, 'face', unique_id)
            elif self.classes[class_id] in self.ALLOWED_CLASSES:
                score = float(out[1][0][obj])
                if score > .5:
                    bbox = [float(v) for v in out[2][0][obj]]
                    x = int(bbox[1] * cols)
                    y = int(bbox[0] * rows)
                    width = int(bbox[3] * cols)
                    height = int(bbox[2] * rows)
                    self.write_to_disk(image, x, y, width, height, self.classes[class_id], unique_id)

    def write_to_disk(self, image, x, y, width, height, obj_class, unique_id=None):
        cropped_img = image[y: height, x: width]
        file_save_path = '{}/{}/{}.jpg'.format(self.media_root, obj_class, uuid4())
        cv2.imwrite(file_save_path, cv2.cvtColor(cropped_img, cv2.COLOR_RGB2BGR))
        file_name = file_save_path.split(self.media_root)[1]
        if unique_id is not None:
            if unique_id in self.images_saved_to_disk:
                self.images_saved_to_disk[unique_id].append(file_name)
            else:
                self.images_saved_to_disk[unique_id] = [file_name]
        return file_name


if __name__ == '__main__':
    # Some examples how to use the classifier
    # classifier = Classifier()
    # classifier.classify_video('./video-sample.mp4')
    # classifier.classify_video('./tf_models/demo_data/road.mp4')
    # sample_img = cv2.imread('sample.jpg')
    # classifier.classify_image(sample_img)
    pass
