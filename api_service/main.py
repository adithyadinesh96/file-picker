from flask import Flask, request, jsonify

from bucket import Bucket
from file import can_grantor_give_access, grant_file_access, user_has_access_to_file, get_file
from job import create_job
from gevent.pywsgi import WSGIServer
app = Flask(__name__)


def get_files_in_folder(folder_id, credentials, service=None):
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])

    all_files = []
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # It's a folder, so recurse into it
            all_files.extend(get_files_in_folder(file['id'], credentials, service))
        else:
            all_files.append(file)

    return all_files


@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    file_ids = data.get('file_ids', [])
    folder_ids = data.get('folder_ids', [])
    user_id = request.user_info.get('user_id')  # Assuming authentication middleware has added this id after validation
    drive_name = data['drive_name']

    for file_id in file_ids:
        create_job(file_id, user_id, drive_name)

    for folder_id in folder_ids:
        file_list = get_files_in_folder(folder_id)
        for file in file_list:
            create_job(file['id'], user_id, drive_name)

    return jsonify({"message": f"Jobs created for requested files and folders"}), 200


@app.route('/grant_file_access', methods=['POST'])
def grant_access():
    data = request.json
    file_id = data.get('file_id')
    grantee_user_id = data.get('grantee_user_id')  # User to receive access
    grantor_user_id = request.user_info.get('user_id')  # User granting access

    if not can_grantor_give_access(file_id=file_id, grantor_user_id=grantor_user_id):
        return jsonify({"error": "Unauthorized Request!"}), 400

    grant_file_access(file_id=file_id, grantee_user_id=grantee_user_id)
    return jsonify({"error": "Successfully Granted Request"}), 400


@app.route('/query_file', methods=['GET'])
def query_file():
    user_id = request.user_info.get('user_id')  # Assuming authentication middleware has added this id after validation
    file_id = request.args.get('file_id')

    if user_has_access_to_file(user_id, file_id):
        file_data = Bucket('BUCKET_NAME').get_file(file_id)
        return jsonify({"file_data": file_data}), 200
    else:
        return jsonify({"error": "Access denied or file does not exist."}), 403


@app.route('/status', methods=['GET'])
def query_file():
    user_id = request.user_info.get('user_id')  # Assuming authentication middleware has added this id after validation
    file_id = request.args.get('file_id')
    if user_has_access_to_file(user_id, file_id):
        file_data = get_file(file_id=file_id, user_id=user_id)
        if not file_data:
            return jsonify({"error": "Access denied or file does not exist."}), 403
        return jsonify({"status": file_data[2]}), 200
    else:
        return jsonify({"error": "Access denied or file does not exist."}), 403


if __name__ == '__main__':
    _port = 5000
    WSGIServer(listener=("", _port), application=app).serve_forever()
