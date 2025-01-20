# ComfyUI-auto

ComfyUI docker image with some extras

My idea is to have a ComfyUI docker image, which contains everything I need to directly run it in runpod.io.
Theoretically it should run in other container hosts as well, since there is no runpod specific code involved.

If you want to run it yourself and make some modifications, you can just fork this repo,
make your changes and the included github action will build your modified image automatically if you create a release

Models need to be downloaded, after the Container is started. For that you need to open an ssh session and run `model_manager`.
It's an interactive tool to manage the downloaded models.

You can access comfyui and the model_manager like this: `ssh root@<ip> -p <image-ssh-port> -L:8188:localhost:8188`. You can then access ComfyUI over `localhost:8188`.
