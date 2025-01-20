from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Tree
from textual.widgets.tree import TreeNode
import requests
from concurrent.futures import ThreadPoolExecutor
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from pathlib import Path
import rich
import typer

OUTPUT_DIR = Path("output")
# TODO: The size should be determined automatically
MODEL_DATA = {
    "checkpoints/": {
        "sdxl/": {
            "juggernaut-xl_11.safetensors": {
                "type": "civitai",
                "url": "https://civitai.com/api/download/models/782002?type=Model&format=SafeTensor&size=full&fp=fp16",
                "size": "6.6GB",
            },
        },
        "flux/": {
            "1-dev-fp8.safetensors": {
                "type": "huggingface",
                "auth": True,
                "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors?download=true",
                "size": "17.2GB",
            },
        },
    },
    "controlnet/": {
        "sdxl/": {
            "controlnet/": {
                "qr-monster-v1.safetensors": {
                    "type": "huggingface",
                    "auth": False,
                    "url": "https://huggingface.co/monster-labs/control_v1p_sdxl_qrcode_monster/resolve/main/diffusion_pytorch_model.safetensors?download=true",
                    "size": "5.0GB",
                },
            },
            "t2i/": {
                "canny-fp16.safetensors": {
                    "type": "huggingface",
                    "auth": False,
                    "url": "https://huggingface.co/TencentARC/t2i-adapter-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.fp16.safetensors?download=true",
                    "size": "150MB",
                },
                "depth-fp16.safetensors": {
                    "type": "huggingface",
                    "auth": False,
                    "url": "https://huggingface.co/TencentARC/t2i-adapter-depth-midas-sdxl-1.0/resolve/main/diffusion_pytorch_model.fp16.safetensors?download=true",
                    "size": "150MB",
                },
                "sketch-fp16.safetensors": {
                    "type": "huggingface",
                    "auth": False,
                    "url": "https://huggingface.co/TencentARC/t2i-adapter-sketch-sdxl-1.0/resolve/main/diffusion_pytorch_model.fp16.safetensors?download=true",
                    "size": "150MB",
                },
                "openpose-fp32.safetensors": {
                    "type": "huggingface",
                    "auth": False,
                    "url": "https://huggingface.co/Adapter/t2iadapter/resolve/main/openpose_sdxl_1.0/diffusion_pytorch_model.safetensors?download=true",
                    "size": "150MB",
                },
            },
        },
    },
}


def init_model_data(models: dict[str, Any], output_dir: Path, subpath: str = ""):
    """Gathers information about the models, before processing."""
    for key, value in models.items():
        if key[-1] == "/":
            init_model_data(value, output_dir, subpath + key)
            value["_ui"] = {"selected": 0, "downloaded": False}
        else:
            value["filename"] = subpath + key

            if (output_dir / value["filename"]).exists():
                value["_ui"] = {"selected": 2, "downloaded": True}
            else:
                value["_ui"] = {"selected": 0, "downloaded": False}


class ModelTree(Tree):
    """A Textual widget to display the model list."""

    @classmethod
    def from_model_dict(cls, title: str, id: str, models: dict) -> "ModelTree":
        tree = ModelTree(title, id=id)
        tree.root.expand()
        tree.fill_model_data(models)

        return tree

    def fill_model_data(self, models: dict) -> None:
        self._fill_branch(self.root, models)

    def _fill_branch(self, tree_node: TreeNode, model_subset: dict[str, Any]):
        for key, value in model_subset.items():
            if key == "_ui":
                continue

            if key[-1] == "/":
                new_node = tree_node.add(
                    self.get_node_state_text((key, value), 0),
                    expand=True,
                    data=(key, value),
                )
                self._fill_branch(new_node, value)
                self._update_parents(new_node)
            else:
                new_node = tree_node.add_leaf(
                    self.get_node_state_text((key, value), value["_ui"]["selected"]),
                    data=(key, value),
                )

    def get_node_state_text(self, data: tuple[str, dict] | None, state: int) -> str:
        assert data is not None
        key, value = data

        text = ""
        if state == 2:
            text += "[bright_black][[/bright_black][green]x[/green][bright_black]][/bright_black]"
        elif state == 1:
            text += "[bright_black][[/bright_black][yellow]~[/yellow][bright_black]][/bright_black]"
        else:
            text += "[bright_black][[/bright_black] [bright_black]][/bright_black]"

        text += "[green]" * value["_ui"]["downloaded"] + f" {key}"
        text += f" ({value.get('size', 'N/a')})" * ("size" in value)

        return text

    def _update_parents(self, tree_node: TreeNode):
        if tree_node.data is None:
            return

        state = 0
        all = True
        for node in tree_node.children:
            data: tuple[str, dict] | None = node.data
            assert data is not None
            key, value = data

            if key == "_ui":
                continue

            selected = value["_ui"]["selected"]

            if selected > 0:
                state = 1
            if selected < 2:
                all = False

        if all:
            state = 2

        data: tuple[str, dict] | None = tree_node.data
        assert data is not None
        key, value = data

        tree_node.label = self.get_node_state_text(data, state)
        value["_ui"]["selected"] = state

        if tree_node.parent:
            self._update_parents(tree_node.parent)

    def _update_children(self, tree_node: TreeNode, state: int):
        for node in tree_node.children:
            data: tuple[str, dict] | None = node.data
            assert data is not None
            key, value = data

            if key == "_ui":
                continue

            node.label = self.get_node_state_text(data, state)
            value["_ui"]["selected"] = state
            if key[-1] == "/":
                self._update_children(node, state)

    def toggle_model(self, tree_node: TreeNode):
        data: tuple[str, dict] | None = tree_node.data
        assert data is not None
        key, value = data

        selected = value["_ui"]["selected"]

        if selected <= 1:
            selected = 2
        elif selected == 2:
            selected = 0

        tree_node.label = self.get_node_state_text(data, selected)
        value["_ui"]["selected"] = selected

        if key[-1] == "/":
            self._update_children(tree_node, selected)
        else:
            assert tree_node.parent is not None
            self._update_parents(tree_node.parent)


class ModelManagerApp(App):
    """A Textual app to manage model downloads"""

    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("s", "select_model", "Select model"),
        ("d", "start_download", "Start download"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""

        yield Header()
        yield Footer()
        yield ModelTree.from_model_dict("Models", id="tree", models=MODEL_DATA)

    def action_select_model(self) -> None:
        """Selects the current item in the tree."""
        tree: ModelTree = self.query_one("#tree")  # type: ignore
        assert tree.cursor_node is not None
        tree.toggle_model(tree.cursor_node)

    def action_start_download(self) -> None:
        """Starts to download all selected models."""

        self.app.exit("download")


def get_changes(models: dict) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    new = []
    obsolete = []
    for key, value in models.items():
        if key == "_ui":
            continue

        if key[-1] == "/":
            i_new, i_obsolete = get_changes(value)
            new.extend(i_new)
            obsolete.extend(i_obsolete)
        else:
            if value["_ui"]["selected"] and not value["_ui"]["downloaded"]:
                new.append(value)
            elif not value["_ui"]["selected"] and value["_ui"]["downloaded"]:
                obsolete.append(value)

    return new, obsolete


def download_file_with_progress(
    item: dict[str, Any], progress: Progress, task_id, output_dir: Path
) -> str:
    filename = output_dir / item["filename"]
    filename.parent.mkdir(parents=True, exist_ok=True)
    url = item["url"]

    progress.start_task(task_id)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        progress.update(task_id, total=total_size)

        with filename.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                progress.update(task_id, advance=len(chunk))

    return url


def download_with_progress(download_list, output_dir: Path):
    with Progress(
        TextColumn("[bold blue]{task.fields[filename]}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        tasks = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            for item in download_list:
                task_id = progress.add_task(
                    "downloading", filename=item["filename"], start=False
                )
                tasks[
                    executor.submit(
                        download_file_with_progress, item, progress, task_id, output_dir
                    )
                ] = task_id

            for future, task_id in tasks.items():
                try:
                    future.result()
                except Exception as e:
                    progress.log(f"[red]Error downloading {future}: {e}")


def delete_files(file_list, output_dir: Path):
    for item in file_list:
        rich.print(f"[red]Deleting {item['filename']}")
        (output_dir / item["filename"]).unlink()


def main(output_dir: Path = OUTPUT_DIR):

    init_model_data(MODEL_DATA, output_dir)
    app = ModelManagerApp()
    result = app.run()

    if result != "download":
        return

    new, obsolete = get_changes(MODEL_DATA)

    if obsolete:
        rich.print("[yellow]Deleting old models...")
        delete_files(obsolete, output_dir)

    if new:
        rich.print("[yellow]Downloading new models...")
        download_with_progress(new, output_dir)

    rich.print("[green]Done!")


if __name__ == "__main__":
    typer.run(main)
