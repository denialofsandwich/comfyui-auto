#!/bin/bash

pushd $(dirname $0)

echo "Get endpoint..."
ENDPOINT=$(runpodctl get pod -a | grep comfyui-auto | cut -f12 | sed -rn 's/^.*,([0-9.:]+)->22.*/\1/p')

IP=$(echo $ENDPOINT | cut -d':' -f 1)
PORT=$(echo $ENDPOINT | cut -d':' -f 2)

echo $IP $PORT

echo "Upload Userdata..."
rsync -avz -e "ssh -p $PORT" --delete --no-owner --no-group --exclude ".git/" --exclude "default/ComfyUI-Manager/cache/" "comfyui_user/" "root@$IP:/data/comfyui_user"

echo "Open shell..."
ssh root@$IP -p $PORT -L 8188:localhost:8188

echo "Download Userdata..."
rsync -avz -e "ssh -p $PORT" --delete --no-owner --no-group --exclude ".git/" --exclude "default/ComfyUI-Manager/cache/" root@$IP:/data/comfyui_user/ comfyui_user/
