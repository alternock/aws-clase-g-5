from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from os import environ
import boto3

app = Flask(__name__)
CORS(app)


app.config["AWS_ACCESS_KEY"] = environ.get("AWS_ACCESS_KEY")
app.config["AWS_SECRET_KEY"] = environ.get("AWS_SECRET_KEY")


bucket_name = "mybucketoplesk"
key = "avatar_x.png"

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config["AWS_ACCESS_KEY"],
    aws_secret_access_key=app.config["AWS_SECRET_KEY"]
)



@app.route("/", methods=["GET"])
def fn_show():
    objects = s3.list_objects(Bucket=bucket_name)['Contents']
    ls = []
    for obj in objects:
        ls.append(s3.generate_presigned_url("get_object", Params={"Bucket":bucket_name, "Key":obj["Key"]}))
    return render_template('index.html', image_urls=ls)



@app.route("/upload", methods=["GET"])
def fn_show_upload():
    return render_template("upload.html")



@app.route("/upload", methods=["POST"])
def fn_add_upload():
    content = ""
    image = request.files["image"]
    if image:
        s3.upload_fileobj(image,bucket_name,image.filename)
        content = "success..."
        return render_template("index.html", msg = content)
    
    content = "fail..."
    return render_template("index.html", msg = content)



if __name__ == "__main__":
    app.run(debug=True)