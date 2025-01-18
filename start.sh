#!/bin/bash

# ENV vars needed:
# PUBLIC_KEY: Automatically set by runpod
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# S3_BUCKET_NAME
# S3_URL

echo "pod started"

if [[ "$PUBLIC_KEY" ]]; then
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  cd ~/.ssh
  echo "$PUBLIC_KEY" >>authorized_keys
  chmod 700 -R ~/.ssh
  cd /
  service ssh start
fi

if [[ "$S3_BUCKET_NAME" ]]; then
  ln -s /data/comfyui_user /ComfyUI/user
  mkdir -p /data/comfyui_user ~/.aws

  cat >~/.aws/credentials <<EOM
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOM

  cat >~/.s3default <<EOM
export S3_BUCKET_NAME="$S3_BUCKET_NAME"
export S3_URL="$S3_URL"
EOM

  cat >~/.bashrc <<EOM
source ~/.s3default
EOM

fi

/ComfyUI/venv/bin/python3 /ComfyUI/main.py
