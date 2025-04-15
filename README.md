# ComfyUI-auto

A ComfyUI Docker image with preinstalled tools.

## Notice
This branch is also containing all resources for my Beyond Dall-E talk at PyConDE 2025.
The Workflow files and images are located under `/comfyui_user_default/workflows` and `/comfyui_user_default/input`.
I reduced the list of models in the model manager to only contain the models I used during the presentation.

I also created a [Runpod template](https://runpod.io/console/deploy?template=ry0man5whx&ref=codsib8t).

## Idea
My idea is to have a ComfyUI docker image, which contains everything I need to directly run it in [runpod.io](https://www.runpod.io).
It is designed to be deployed fast even if you delete the volumes, to minimize the cost.

If you want to run a customized version yourself, just fork the repo. A new image is being built automatically, if you create a new release using GitHub Actions.

## How to use

You need to create a runpod template and set the following:
- **Container Image:** `ghcr.io/denialofsandwich/comfyui-auto:v0.1.18-pyconde25`
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

The also is a wrapper (`runpod_connect.sh`) to automatically connect to the instance. It requires `runpodctl` to be installed to work properly.

Once you are connected you need to download models. I provided a tool to make the download easy, which opens a terminal ui with a preselected list of models ready to download directly into the pod.
Just run the `model_manager` command in your ssh session, and you can select the models you need.

## References

Here are some repos, I've used as a reference.

- <https://github.com/ValyrianTech/ComfyUI_with_Flux>
- <https://github.com/comfyanonymous/ComfyUI>
- <https://diffusionillusions.com/> (The "flip image" illusion I've replicated)
