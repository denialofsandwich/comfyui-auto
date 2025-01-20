#!/bin/bash

# ENV vars needed:
# PUBLIC_KEY: Automatically set by runpod
# HUGGINGFACE_TOKEN: Needed for Flux
# CIVITAI_TOKEN: Required for downloading all civitai models

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

cat >~/.credentials <<EOM
export HUGGINGFACE_TOKEN="$HUGGINGFACE_TOKEN"
export CIVITAI_TOKEN="$CIVITAI_TOKEN"
EOM

cat >~/.bashrc <<EOM
source ~/.credentials
alias model_manager='/ComfyUI/venv/bin/python3 /ComfyUI/model_manager/main.py --output-dir /data/models'
EOM

/ComfyUI/venv/bin/python3 /ComfyUI/main.py
