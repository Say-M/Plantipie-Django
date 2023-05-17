from django.core.files.storage import FileSystemStorage

def upload_file(location, base_url, file):
    fss = FileSystemStorage(location=location, base_url=base_url)
    filename = fss.save(file.name, file)
    uploaded_file_url = fss.url(filename)
    return uploaded_file_url