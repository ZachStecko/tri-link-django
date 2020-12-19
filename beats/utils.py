from django.http import HttpResponse
from wsgiref.util import FileWrapper
from pathlib import Path
from .models import Customer
import os

def handle_uploaded_file(f,u):
    ext = os.path.splitext(f.name)[1]

    dirName = 'user_' + str(u)
    if not os.path.exists(dirName):
        os.mkdir('Magic/Audio/' + dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")

    destination = open('Magic/Audio/' + dirName + '/user_'+str(u)+'%s'%(ext), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_uploaded_image(f,u):
    ext = os.path.splitext(f.name)[1]

    dirName = 'user_' + str(u)
    if not os.path.exists(dirName):
        os.mkdir('Magic/Image/' + dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")

    destination = open('Magic/Image/' + dirName + '/user_'+str(u)+'%s'%(ext), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

#3
def download(request):
    send = request
    random_value = Customer.objects.get(user = send).random_id
    file_path = './Magic/Video/'+random_value+'user_'+str(send)+'.mp4'
    my_file = Path(file_path)

    if my_file.is_file():
        #exists
        try:
            wrapper = FileWrapper(open(file_path, 'rb'))
            response = HttpResponse(wrapper, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception as e:
            return HttpResponse(content=204)

#4
def deleteTheFile(request):
    send = request
    random_value = Customer.objects.get(user = send).random_id
    video_path = './Magic/Video/'+random_value+'user_'+str(send)+'.mp4'
    my_video = Path(video_path)

    try:
        if my_video.is_file():
            pathToDelete = video_path
            os.remove(pathToDelete)
    except Exception as e:
            return None        