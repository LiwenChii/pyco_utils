from . import (
    app,
    request,
    json_response,
)


def upload_file(file, path='.'):
    filename = file.filename
    filepath = '{}/{}'.format(path, filename)
    file.save(filepath)
    file.seek(0)
    return path


@app.route('/upload/images', methods=['POST'])
def upload_images():
    files = request.files
    data = [upload_file(f) for f in files.values()]
    return json_response(True, data=data)
