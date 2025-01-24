#!/bin/bash

pushd $(dirname $0)

echo "Get endpoint..."
ENDPOINT=$(runpodctl get pod -a | cut -f12 | sed -rn '2{s/^.*,([0-9.:]+)->22.*/\1/p}')

IP=$(echo $ENDPOINT | cut -d':' -f 1)
PORT=$(echo $ENDPOINT | cut -d':' -f 2)

echo $IP $PORT

echo "Upload userdata..."
rsync -avz -e "ssh -p $PORT" --delete --no-owner --no-group --exclude ".git/" --exclude "default/ComfyUI-Manager/cache/" "comfyui_user/" "root@$IP:/data/comfyui_user"

echo "Open shell..."
ssh root@$IP -p $PORT -L 8188:localhost:8188

echo "Download userdata..."
rsync -avz -e "ssh -p $PORT" --delete --no-owner --no-group --exclude ".git/" --exclude "default/ComfyUI-Manager/cache/" root@$IP:/data/comfyui_user/ comfyui_user/
