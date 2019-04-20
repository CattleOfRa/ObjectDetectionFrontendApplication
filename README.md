# ObjectDetectionFrontendApplication

## Introduction

This is a simple frontend application for performing object detection using tensorflow on certain objects of choice. At
the moment of writing, the objects are pre-defined within the code, though an option to allow users to select objects
of interest will be added in the future. <br />

[SSD MobileNet](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz)
pre-trained model was used for our object detector which was trained on the COCO dataset on 183 different classes. For
all the supported classes see the
[labels file](https://github.com/CattleOfRa/ObjectDetectionFrontendApplication/blob/master/App/tf_models/labels.txt).

## Quick Start

Please ensure you have Python 2.7, virtualenv and pip already installed in your system.

Download the repository and cd into the project.

```
git clone https://github.com/CattleOfRa/ObjectDetectionFrontendApplication
cd ObjectDetectionFrontendApplication/
```

Create a new virtual environment and install the necessary packages.

```
virtualenv .
source bin/activate
pip install -r requirements.txt
```

CD into the DJango App and start the web-server.

```
cd App/
python manage.py runserver
```

If no errors, the server will start and the frontend will be available from <http://127.0.0.1:8000> to test.

## Tech Roadmap

Below are some of the components that will be added in the future.

- [ ] Selecting objects of interest
- [ ] Improve interface to view detected objects and provide more relevant information:
    - [ ] Individual Object Confidence Level
    - [ ] Object inference time
    - [ ] Overall stats (possibly generate graphs to evaluate model performance)
- [ ] Add interface to compare performance of different models 
- [ ] Add interface for re-training models
- [ ] Add tools to prepare and generate dataset for training
- [ ] Extend application to support object classification (data preparation, training and testing)
