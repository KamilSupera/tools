from dotenv import load_dotenv

import os
import logging

import setup_boto

load_dotenv()
logging.basicConfig(level=logging.INFO)


def get_files_list():
    files = os.listdir(os.getenv("FILE_PATH"))
    client = setup_boto.setup_boto3_client("s3")

    errors = []
    successful  = []

    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            send_file_again = False

            logging.info(f"Tried to upload file: {file}")

            if(setup_boto.upload_file_to_s3(client, file)):
                successful.append(file)
            else:
                send_file_again = True

            if (send_file_again):
                if(setup_boto.upload_file_to_s3(client, file)):
                    logging.info(f"Tried to upload again file: {file}")
                    successful.append(file)
                else:
                    errors.append(file)

    return successful, errors

if __name__ == '__main__':
    successful, errors = get_files_list()

    print(f"Uploaded {successful} to S3")
    print(f"Failed to upload {errors} to S3")
