from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Tree
from textual.widgets.tree import TreeNode


MODEL_DATA = {
    "checkpoints/": {
        "sdxl/": {
            "juggernaut-xl_11.safetensors": {
                "type": "civitai",
                "url": "https://civitai.com/api/download/models/782002?type=Model&format=SafeTensor&size=full&fp=fp16",
            },
        },
        "flux/": {
            "1-dev-fp8.safetensors": {
                "type": "huggingface",
                "auth": True,
                "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors?download=true",
            },
        },
    },
}


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
            if key[-1] == "/":
                new_node = tree_node.add(
                    f"[bright_black][[/bright_black][green] [/green][bright_black]][/bright_black] {key}",
                    expand=True,
                )
                self._fill_branch(new_node, value)
            else:
                tree_node.add_leaf(
                    f"[bright_black][[/bright_black][green]x[/green][bright_black]][/bright_black] {key}",
                    data=(key, value),
                )


class ModelManagerApp(App):
    """A Textual app to manage model downloads"""

    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("s", "select_model", "Select model"),
        ("d", "start_download", "Start download"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""

        tree = ModelTree("test")
        tree.root.expand()
        characters = tree.root.add("Checkpoints", expand=True)
        characters.add_leaf("[[green]x[/green]] SDXL Juggernaut XI")
        characters.add_leaf("[[green] [/green]] Flux Dev")
        controlnet = tree.root.add("ControlNet", expand=True)
        controlnet.add_leaf("[[green]x[/green]] SDXL Canny")
        controlnet.add_leaf("[[green] [/green]] SDXL Depth")

        yield Header()
        yield Footer()
        yield ModelTree.from_model_dict("Models", id="tree", models=MODEL_DATA)

    def action_select_model(self) -> None:
        """Selects the current item in the tree."""
        tree: Tree[str] = self.query_one("#tree")

        self.title = tree.cursor_node.data

    def action_start_download(self) -> None:
        """Starts to download all selected models."""
        tree: Tree[str] = self.query_one("#tree")

        self.title = tree.cursor_node.label


if __name__ == "__main__":
    app = ModelManagerApp()
    app.run()
