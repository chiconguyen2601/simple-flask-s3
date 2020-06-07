from flask import Flask, render_template, request

from werkzeug.utils import secure_filename
import boto3

app     = Flask(__name__, template_folder='/home/oneadmin/Desktop/working/flask-s3/')
app.config.from_object("config")

access_key = "96WX2Q4HUE8KG3C0LEIZ"
secret_key = "V3vdmwdAHwBPT5cLeRLNjVq8aICCdBXzt6aaYxnx"
endpoint_url = "http://ceph3:7480"
bucket_name = "chiconguyen"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=["POST"])
def upload():
	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file:
        file.filename = secure_filename(file.filename)
        # output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        # s3 = boto3.resource('s3',
        #                 endpoint_url=endpoint_url,
        #                 aws_access_key_id=access_key,
        #                 aws_secret_access_key=secret_key)
        # bucket = s3.Bucket(bucket_name)
        s3 = boto3.client(
		   "s3",
		   endpoint_url=endpoint_url,
		   aws_access_key_id=access_key,
		   aws_secret_access_key=secret_key
		)
        # bucket.upload_file(Filename=file,
	       #                 Key=file.filename)
        # bucket.put_object(bucket_name,
        #               Key=file.filename,
        #               Body=file)
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename
        )
        # bucket.Object(file.filename).put(Body=file.read())
        # file_key = bucket.get_key(file.filename)

        # return str(file_key.generate_url(0, query_auth=False, force_http=True))
        url = s3.generate_presigned_url(
            'get_object', 
            Params = { 
                      'Bucket': bucket_name, 
                      'Key': file.filename, }, 
            ExpiresIn = 86400, )
        return url

    else:
        return redirect("/")

if __name__ == "__main__":
    app.run()