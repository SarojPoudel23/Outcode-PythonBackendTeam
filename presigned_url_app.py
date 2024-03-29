from flask import Flask, request, jsonify
import boto3
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS credentials
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

# Initialize Boto3 client for S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


# Function to generate presigned URLs for S3 bucket objects
def generate_presigned_url(file_name, bucket_name, expiration_time):
    """
    Generate presigned URL
    """
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": file_name,
            },
            ExpiresIn=expiration_time,
        )

        return presigned_url

    except Exception as e:
        logger.error(f"Error generating presigned URL: {str(e)}")
        return None


# Route for generating presigned URL
@app.route('/presigned-url', methods=['GET'])
def presigned_url():
    file_name = request.args.get('file_name')
    if not file_name:
        return jsonify({"error": "File name not provided"}), 400

    bucket_name = "YOUR_S3_BUCKET_NAME"
    expiration_time = 3600  # Expiration time in seconds (1 hour)

    presigned_url = generate_presigned_url(file_name, bucket_name, expiration_time)
    if presigned_url:
        return jsonify({"presigned_url": presigned_url}), 200
    else:
        return jsonify({"error": "Failed to generate presigned URL"}), 500


if __name__ == '__main__':
    app.run(debug=True)
