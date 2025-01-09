#!/bin/bash

# ENV vars needed:
# PUBLIC_KEY: Automatically set by runpod
# AWS_ACCESS_KEY_ID
# AWS_ACCESS_KEY_KEY
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

  mkdir -p /tmp/s3mount_cache
  s3fs $S3_BUCKET_NAME:/ /data \
    -o url=$S3_URL \
    -o use_path_request_style \
    -o use_cache=/tmp/s3mount_cache \
    -o stat_cache_expire=300 \
    -o enable_noobj_cache \
    -o multipart_size=52 \
    -o parallel_count=5
fi

/ComfyUI/venv/bin/python3 /ComfyUI/main.py
