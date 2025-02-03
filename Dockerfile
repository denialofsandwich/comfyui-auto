ARG CUDA_VERSION="12.6.3"
ARG UBUNTU_VERSION="24.04"
ARG DOCKER_FROM=nvidia/cuda:$CUDA_VERSION-base-ubuntu$UBUNTU_VERSION

# Base NVidia CUDA Ubuntu image
FROM $DOCKER_FROM AS base

# Install Python plus openssh, which is our minimum set of required packages.
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get install -y --no-install-recommends openssh-server openssh-client git git-lfs wget vim zip unzip curl lsof htop rsync ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/cuda/bin:${PATH}"

ARG PYTORCH="2.4.0"
ARG CUDA="126"
RUN git clone https://github.com/comfyanonymous/ComfyUI.git && \
    cd /ComfyUI && \
    python3 -m venv venv && \
    /ComfyUI/venv/bin/pip3 install -r requirements.txt && \
    /ComfyUI/venv/bin/pip3 install --no-cache-dir -U torch==$PYTORCH torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu$CUDA

RUN cd /ComfyUI/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git && \
    git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git && \
    git clone https://github.com/crystian/ComfyUI-Crystools.git && \
    /ComfyUI/venv/bin/pip3 install -r ComfyUI-Crystools/requirements.txt && \
    git clone https://github.com/kijai/ComfyUI-KJNodes.git && \
    /ComfyUI/venv/bin/pip3 install -r ComfyUI-KJNodes/requirements.txt && \
    git clone https://github.com/yolain/ComfyUI-Easy-Use.git && \
    /ComfyUI/venv/bin/pip3 install -r ComfyUI-Easy-Use/requirements.txt && \
    git clone https://github.com/WASasquatch/was-node-suite-comfyui.git && \
    /ComfyUI/venv/bin/pip3 install -r was-node-suite-comfyui/requirements.txt && \
    git clone https://github.com/chflame163/ComfyUI_LayerStyle.git && \
    /ComfyUI/venv/bin/pip3 install -r ComfyUI_LayerStyle/requirements.txt && \
    git clone https://github.com/storyicon/comfyui_segment_anything && \
    /ComfyUI/venv/bin/pip3 install -r comfyui_segment_anything/requirements.txt && \
    git clone https://github.com/Acly/comfyui-inpaint-nodes
    #git clone https://github.com/Gourieff/comfyui-reactor-node.git && \
    #/ComfyUI/venv/bin/pip3 install -r comfyui-reactor-node/requirements.txt

COPY --chmod=755 start.sh /start.sh
COPY --chmod=755 extra_model_paths.yaml /ComfyUI/extra_model_paths.yaml
COPY --chmod=755 model_manager/ /ComfyUI/model_manager/

RUN /ComfyUI/venv/bin/pip3 install -r /ComfyUI/model_manager/requirements.txt

WORKDIR /workdir
EXPOSE 7860

CMD [ "/start.sh" ]
