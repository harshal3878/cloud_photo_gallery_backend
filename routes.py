from flask import Blueprint, jsonify, request
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import random
import string


main = Blueprint('main', __name__)

# AWS S3 configuration
S3_BUCKET = 'cloud-gallery-bucket'
S3_FOLDER = 'harshal_2509/'  # Folder where the images are stored in the bucket
S3_REGION = 'us-west-2'  # Replace with your S3 region
filename  = "Screenshot1.png"
# Initialize boto3 client
s3_client = boto3.client('s3', region_name=S3_REGION)

@main.route('/')
def home():
    return "Hello world, speed 1 terrabytes mermory 1 zhettabytes!"

@main.route('/get-image')
def get_image():
    try:
        # Generate a presigned URL for the requested image
        presigned_url = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': S3_BUCKET,
                                                                 'Key': f'{S3_FOLDER}{filename}'},
                                                         ExpiresIn=360)  
        
        print("presigned_url: "+presigned_url)
        # Redirect to the presigned S3 URL
        return presigned_url

    except Exception as e:
        return jsonify({'error': str(e)}), 500




#get grid of images stored for user.    
@main.route('/browse')
def get_images():
    try:
        initial_image_list = s3_client.list_objects(
        Bucket=S3_BUCKET,
        MaxKeys=20,
        Prefix=S3_FOLDER)
        image_keys = []
        image_presigned_urls = []
        for image in initial_image_list["Contents"]:
            image_key = image["Key"] 
            print(image_key)
            if image_key != S3_FOLDER:
                image_keys.append(image_key)
                presigned_url = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': S3_BUCKET,
                                                                 'Key': image_key },
                                                         ExpiresIn=360)
                image_presigned_urls.append(presigned_url)
        return jsonify({'success': True, 'message': image_presigned_urls}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 


@main.route('/upload-image', methods=['POST'])
def upload_image():
    try:

        # generate random name and Upload to S3        
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(10))
        file = request.files['image']
        image_extension = str(file.filename).split(".")[1]
        print(image_extension)
        print(f"uploading image to :{S3_FOLDER}{random_string}")
        s3_client.upload_fileobj(file, S3_BUCKET, f"{S3_FOLDER}{random_string}.{image_extension}")
        
    except NoCredentialsError:
        print(jsonify({'success': False, 'error': 'Credentials not available'}))
        return jsonify({'success': False, 'error': 'Credentials not available'}), 403
    except ClientError as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)}), 500
    return jsonify({'success': True, 'message': 'File uploaded successfully! 🎉😊'}), 201