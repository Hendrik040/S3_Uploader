import streamlit as st
import boto3
import os
import hashlib
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials and bucket configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'your_access_key')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'your_secret_key')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'hult-unstructured-data-challenge')

# Password for application access
APP_PASSWORD = os.getenv('APP_PASSWORD', 'HultDataPirates-Arrr')

def upload_to_s3(file, bucket, object_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3_client.upload_fileobj(file, bucket, object_name)
        st.success("Upload Successful")
    except NoCredentialsError:
        st.error("Credentials not available")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def list_files_in_folder(bucket, folder):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder)
        if 'Contents' in response:
            return [item['Key'] for item in response['Contents']]
        else:
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

def delete_file(bucket, object_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
        st.success(f"Deleted {object_name} successfully")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == APP_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if "password_correct" in st.session_state:
        return st.session_state["password_correct"]

    # First run, show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    return False

def main():
    st.title("S3 File Manager")
    
    if not check_password():
        st.warning("Please enter the correct password to access the application.")
        return

    # Select team
    team_id = st.selectbox("Select Team", list(range(1, 13)))
    folder = f"team{team_id}/"

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "png", "jpg", "jpeg"])

    # Upload button
    if uploaded_file is not None:
        if st.button("Upload File"):
            object_name = f"{folder}{uploaded_file.name}"
            upload_to_s3(uploaded_file, S3_BUCKET_NAME, object_name)

    # List and delete files
    st.subheader("Files in your folder")
    files = list_files_in_folder(S3_BUCKET_NAME, folder)
    if files:
        for file in files:
            st.write(file)
            if st.button(f"Delete {file}", key=file):
                delete_file(S3_BUCKET_NAME, file)
    else:
        st.write("No files found.")

if __name__ == "__main__":
    main()
