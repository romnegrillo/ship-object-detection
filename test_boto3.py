import boto3
from botocore.config import Config
import os
import time
import configparser

config = configparser.RawConfigParser()
config.read("config.ini")

AWS_ACCESS_KEY = config["General"]["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS = config["General"]["AWS_SECRET_ACCESS"]
BUCKET_NAME = config["General"]["BUCKET_NAME"]

config = Config(connect_timeout=3600, read_timeout=3600)
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_ACCESS,
                  config=config)

# s3.upload_file("./test_upload_image/test_upload.png",
#                BUCKET_NAME, "detected_ships/10-01-2022-10-30-AM-2.png")
# time.sleep(1)
# s3.upload_file("./test_upload_image/test_upload.png",
#                BUCKET_NAME, "detected_ships/10-01-2022-10-45-AM-3.png")
# time.sleep(1)
# s3.upload_file("./test_upload_image/test_upload.png",
#                BUCKET_NAME, "detected_ships/10-01-2022-12-30-PM-4.png")
# time.sleep(1)
# s3.upload_file("./test_upload_image/test_upload.png",
#                BUCKET_NAME, "detected_ships/10-01-2022-09-30-PM-5.png")
# time.sleep(1)

# s3.download_file(BUCKET_NAME, "detected_ships/10-01-2022-10-45-AM-2.png",
#                  "./test_download_image/10-01-2022-10-45-AM-2.png")
# print(os.path.exists("test_download_image/10-01-2022-10-30-AM-2.png"))

response = s3.list_objects(Bucket=BUCKET_NAME)

# for content in response.get('Contents', []):
#     print(content["Key"])

image_dict = {}
for content in response.get('Contents', []):
    image_dict[content["Key"]] = content["LastModified"]

img_list_sorted = sorted(
    image_dict.items(), key=lambda item: item[1], reverse=True)
print(img_list_sorted[0][0])
