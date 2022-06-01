# bucket-migration
Bucket-migration is a repository that copies the content of a bucket to another.

## Instalation
### Setup prerequisites
1. Requirements files are files containing a list of items to be installed using [pip](https://pip.pypa.io/en/stable/cli/pip_install/#pip-install) install like so: <br />
```bash 
python -m pip install -r requirements.txt
```
2. Set up AWS credentials (in e.g. ~/.aws/credentials):<br />
```bash
aws configure set aws_access_key_id "$aws_access_id" --profile $profile
aws configure set aws_secret_access_key "$aws_secret" --profile $profile 
aws configure set region "$aws_region" --profile $profile
export AWS_PROFILE=$profile
```

## Usage
Set up the buckets details in source/constants.py file.

### Command
```bash
python main.py
```
   

