AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_REGION_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_DEFAULT_ACL = None
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


if request.user.is_authenticated:
        try:
            if request.user.is_authenticated:
                # Handle file upload
                current_user = request.user
                send = current_user.username

                file_path = './Magic/Video/user_'+str(send)+'.mp4'
                my_file = Path(file_path)
                audio = 'Magic/Audio/user_'+str(send)
                img = 'Magic/Image/user_'+str(send)

                try:
                    shutil.rmtree(audio)
                    shutil.rmtree(img)
                except:
                    print("We good")

                if request.method == 'POST':
                    form = DocumentForm(request.POST, request.FILES)
                    if form.is_valid():
                        file_path = './Magic/Video/user_'+str(send)+'.mp4'
                        my_file = Path(file_path)
                        if my_file.is_file():
                            print("hey")
                            os.remove(my_file)

                        fileExts = request.FILES['docfile']
                        audioType = os.path.splitext(fileExts.name)[1]
                        handle_uploaded_file(request.FILES['docfile'], send)
                        audioPathToExport = 'Magic/Audio/user_'+str(send)+'/user_'+str(send)+'%s'%(audioType)
                        audioPathToDelete = 'Magic/Audio/user_'+str(send)

                        fileExt = request.FILES['imgfile']
                        ext = os.path.splitext(fileExt.name)[1]
                        handle_uploaded_image(request.FILES['imgfile'], send)
                        imgPathToExport = 'Magic/Image/user_'+str(send)+'/user_'+str(send)+'%s'%(ext)
                        imgPathToDelete = 'Magic/Image/user_'+str(send)

                        userPath = 'Magic/Video/user_'+str(send)+'.mp4'
                        
                        #export_video().delay()
                        #this needs to be async

                        current_user = request.user
                        userID = current_user.username
                        export_video(audioPathToExport,userPath,imgPathToExport, userID)

                        try:
                            shutil.rmtree(audioPathToDelete)
                            shutil.rmtree(imgPathToDelete)
                        except:
                            print("We good")

                        if my_file.is_file():
                            #exists
                            try:
                                return redirect(thanks)
                            except Exception as e:
                                return None
                        else:
                            # Redirect to the document list after POST
                            return HttpResponseRedirect(reverse('software'))
                else:
                    form = DocumentForm()  # A empty, unbound form

                audio = 'Magic/Audio/user_'+str(send)
                img = 'Magic/Image/user_'+str(send)

                #if my_file.is_file():
                #    os.remove(my_file)
                 # Render list page with the documents and the form  
                return render(request, 'beats/software.html',{'form': form,'my_file': my_file})
        except Customer.DoesNotExist:
                return redirect('signup')
    return redirect('signup')