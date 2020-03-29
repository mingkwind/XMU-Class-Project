from django.http import HttpResponse
from django.http import FileResponse
from .forms import UploadFileForm
from django.shortcuts import render
import os
import time

BASE_DIR="POST"
def download(request,id):
    filename = "download/"+str(1<<id)+".txt"
    file = open(filename,'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename='+filename
    return response

def index(request):
        return HttpResponse("Hello")

def post(request):
    time.process_time()
    if request.method == 'POST':
        before = time.perf_counter()
        name = str(request.FILES['file'])
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],name)
            after = time.perf_counter()
            total = after - before
            return HttpResponse(total)
        else:
            form = UploadFileForm()
        return HttpResponse('OK')
        '''
        f = open(os.path.join(BASE_DIR,file_obj.name),'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        '''
def handle_uploaded_file(f,name):
    with open("post/"+name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
