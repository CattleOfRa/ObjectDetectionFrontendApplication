# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from classifier import Classifier
from uuid import uuid4

import threading
import json

classifier = Classifier(settings.MEDIA_ROOT)
image_type_supported = ['png', 'jpg', 'jpeg']
video_type_supported = ['mp4']


# Create your views here.
def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        unique_id = str(uuid4())
        print('settings.MEDIA_ROOT:{}'.format(settings.MEDIA_ROOT))

        classifier_thread = None
        ext = uploaded_file.name.split('.')[-1]
        if ext in image_type_supported:
            nd_image = classifier.open_image_file_from_disk('{}/{}'.format(settings.MEDIA_ROOT, uploaded_file.name))
            classifier_thread = threading.Thread(
                target=classifier.classify_image,
                args=(nd_image, unique_id))
        elif ext in video_type_supported:
            classifier_thread = threading.Thread(
                target=classifier.classify_video,
                args=('{}/{}'.format(settings.MEDIA_ROOT, uploaded_file.name), unique_id))

        if classifier_thread is not None:
            classifier_thread.start()
            context = {'unique_id': unique_id, }
            return render(request, 'results.html', context)
        else:
            # TODO: Render message to user indication that `file is not supported`.
            pass

    return render(request, 'index.html', {})


def upload_results(request):
    return render(request, 'results.html', {})


def get_images(request):
    if request.method == 'POST':
        unique_id = request.POST.get('unique_id', None)

        laptop = []
        keyboard = []
        face = []

        for image_path in classifier.images_saved_to_disk.get(unique_id, []):
            if 'laptop' in image_path:
                laptop.append(image_path)
            elif 'keyboard' in image_path:
                keyboard.append(image_path)
            elif 'face' in image_path:
                face.append(image_path)
            classifier.images_saved_to_disk[unique_id].remove(image_path)

        images_path = json.dumps({
            'laptop': laptop,
            'keyboard': keyboard,
            'face': face
        })

        return HttpResponse(images_path, content_type="application/json")
