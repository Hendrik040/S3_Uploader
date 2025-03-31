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

    # Select folder option
    folder_option = st.radio("Select folder option", ["First year MBAN", "Dual Degree MBAN", "Custom folder path"])
    
    if folder_option == "First year MBAN":
        st.info("Example: Your files will be stored in 'first_year_mban/your_file_name.pdf'")
        default_folder = "first_year_mban"
        custom_folder = st.text_input("Edit folder path if needed", default_folder)
        folder = f"{custom_folder}/" if custom_folder else ""
    elif folder_option == "Dual Degree MBAN":
        st.info("Example: Your files will be stored in 'dual_degree_mban/your_file_name.pdf'")
        default_folder = "dual_degree_mban"
        custom_folder = st.text_input("Edit folder path if needed", default_folder)
        folder = f"{custom_folder}/" if custom_folder else ""
    else:  # Custom folder path
        st.info("Example: If you previously used 'team1', enter 'team1' to access your files in that folder")
        custom_folder = st.text_input("Enter your folder path", "")
        folder = f"{custom_folder}/" if custom_folder else ""
    
    if not folder:
        st.warning("Please enter a valid folder path")
        return

    st.write(f"Current folder path: {folder}")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "png", "jpg", "jpeg"])

    # Upload button
    if uploaded_file is not None:
        if st.button("Upload File"):
            object_name = f"{folder}{uploaded_file.name}"
            upload_to_s3(uploaded_file, S3_BUCKET_NAME, object_name)

    # List and delete files
    st.subheader("Files in your folder")
    
    # Add explanation about file deletion
    st.info("""
    **How to delete files:**
    1. Your files are listed below
    2. Each file has a 'Delete' button next to it
    3. Click the 'Delete' button to remove the file from the S3 bucket
    4. A success message will appear once the file is deleted
    """)
    
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
