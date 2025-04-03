# ComfyUI-auto

A ComfyUI Docker image with preinstalled tools.

## Idea
My idea is to have a ComfyUI docker image, which contains everything I need to directly run it in [runpod.io](https://www.runpod.io).
It is designed to be deployed fast even if you delete the volumes, to minimize the cost.

If you want to run a customized version yourself, just fork the repo. A new image is being built automatically, if you create a new release using GitHub Actions.

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
- `PUBLIC_KEY`: (automatically set by runpod) Needed if you want to connect via SSH to the pod.
- `HUGGINGFACE_TOKEN` (optional): If you want to download gated models from Huggingface
- `CIVITAI_TOKEN` (optional): If you want to download gated models from CivitAI

You can access ComfyUI like this: `ssh root@<ip> -p <pod-ssh-port> -L:8188:localhost:8188`. You can then access ComfyUI via `localhost:8188`.

The also is a wrapper (`runpod_connect.sh`) to automatically connect to the instance and up/download the user settings and workflows afterwards. It requires `runpodctl` and `rsync` to be installed to work properly.

Once you are connected you need to download models. I provided a tool to make the download easy, which opens a terminal ui with a preselected list of models ready to download directly into the pod.
Just run the `model_manager` command in your ssh session, and you can select the models you need.

## References

Here are some repos, I've used as a reference.

- <https://github.com/ValyrianTech/ComfyUI_with_Flux>
- <https://github.com/comfyanonymous/ComfyUI>
