# S3 File Manager

A Streamlit application that allows users to upload, view, and delete files in an AWS S3 bucket. The application organizes files by team folders (1-12).

## Features

- **Team Selection**: Choose from teams 1-12
- **File Upload**: Drag and drop or browse to select files
- **File Management**: View and delete files in your team's folder
- **Secure**: Uses environment variables for AWS credentials
- **Password Protected**: Access control via password authentication

## Requirements

- Python 3.7+
- Streamlit
- Boto3 (AWS SDK for Python)
- python-dotenv

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your AWS credentials

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
S3_BUCKET_NAME=your_bucket_name_here
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser. You'll need to enter the password to access the application functionality.

## Configuration

The application uses environment variables for AWS credentials. These are loaded from the `.env` file using python-dotenv. For production deployments on Linux or cloud platforms, you can set these environment variables directly in your system or deployment platform.

The default password is set in the application code. For production use, consider moving this to an environment variable as well.

## Security Note

This application uses environment variables to store AWS credentials, which is more secure than hardcoding them. The `.env` file is included in `.gitignore` to prevent accidentally committing your credentials to version control.

For production use, consider using AWS IAM roles when deploying to AWS services, or the appropriate secure credential management for your cloud provider.

## License

MIT
