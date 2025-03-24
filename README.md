# S3 File Manager

A Streamlit application that allows users to upload, view, and delete files in an AWS S3 bucket. The application organizes files by team folders (1-12).

## Features

- **Team Selection**: Choose from teams 1-12
- **File Upload**: Drag and drop or browse to select files
- **File Management**: View and delete files in your team's folder
- **Secure**: Uses AWS credentials for authentication

## Requirements

- Python 3.7+
- Streamlit
- Boto3 (AWS SDK for Python)

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app_ui2.py
```

The application will open in your default web browser.

## Configuration

The application uses AWS credentials for authentication. Make sure to replace the placeholder credentials with your own:

```python
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)
```

## Security Note

For production use, it's recommended to use environment variables or AWS IAM roles instead of hardcoding credentials in the application.

## License

MIT
#   S 3 _ U p l o a d e r  
 