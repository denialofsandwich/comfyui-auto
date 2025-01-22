# ComfyUI-auto

A ComfyUI Docker image with preinstalled tools.

## Idea
My idea is to have a ComfyUI docker image, which contains everything I need to directly run it in [runpod.io](https://www.runpod.io).
It is designed to be deployed fast even if you delete the volumes, to minimize the cost.

If you want to run a customized version yourself, just fork the repo. A new image is being built automatically if you create a new release using GitHub Actions.

## How to use

You need to create a runpod template and set the following:
- **Container Image:** `ghcr.io/denialofsandwich/comfyui-auto:latest` (or the most recent versioned tag)
- **Compute:** Nvidia GPU
- **Type:** Pod
- **Container Disk Size:** ~8GB
- **Volume Disk Path:** `/data`
- **Volume Disk Size:** >16GB
- **Expose TCP Ports:** `22`

The Volume Disk contains all models and user settings.

### Environment Variables
- `PUBLIC_KEY`: (automatically set by runpod) Needed if you want to want to connect via SSH to the pod.
- `HUGGINGFACE_TOKEN` (optional): If you want to download gated models from Huggingface
- `CIVITAI_TOKEN` (optional): If you want to download gated models from CivitAI

You can access ComfyUI like this: `ssh root@<ip> -p <image-ssh-port> -L:8188:localhost:8188`. You can then access ComfyUI over `localhost:8188`.

Once you are connected you need to download models. I provide a tool to download them easy.
Just run the `model_manager` command, and you can select the models you need and download them.

## References

Here are some repos, I've used as a reference.

- <https://github.com/ValyrianTech/ComfyUI_with_Flux>
- <https://github.com/comfyanonymous/ComfyUI>
