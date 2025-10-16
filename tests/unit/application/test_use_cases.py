from collections.abc import Iterable
from impulse.application import use_cases
from copy import copy
import grimp
import graphviz
from grimp.adaptors.graph import ImportGraph
from impulse import ports

SOME_ROOT_PACKAGE = "mypackage"
SOME_MODULE = f"{SOME_ROOT_PACKAGE}.foo"


def build_fake_graph(package_name: str) -> grimp.ImportGraph:
    graph = ImportGraph()
    graph.add_module(package_name)

    graph.add_module(SOME_MODULE)

    for child in ("blue", "green", "yellow", "red"):
        graph.add_module(f"{SOME_MODULE}.{child}")

    graph.add_import(
        importer=f"{SOME_MODULE}.blue.alpha",
        imported=f"{SOME_MODULE}.green",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.green",
        imported=f"{SOME_MODULE}.yellow.beta",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.blue.alpha",
        imported=f"{SOME_MODULE}.red.gamma",
    )
    return graph


class SpyGraphViewer(ports.GraphViewer):
    def __init__(self) -> None:
        self.called_with_dot: graphviz.Digraph | None = None

    def view(self, dot: graphviz.Digraph) -> None:
        self.called_with_dot = dot


class TestDrawGraph:
    def test_draw_graph(self):
        original_sys_path = ["/some/path", "/another/path"]
        sys_path = copy(original_sys_path)
        current_directory = "/cwd"
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            sys_path=sys_path,
            current_directory=current_directory,
            build_graph=build_fake_graph,
            viewer=viewer,
        )

        # The current directory was added to system path.
        assert sys_path == [current_directory, *original_sys_path]
        # The image generation function was called.
        assert viewer.called_with_dot, "Viewer not called."
        assert self._normalize_body(viewer.called_with_dot.body) == {
            "concentrate=true",
            '"mypackage.foo.green"',
            '"mypackage.foo.blue"',
            '"mypackage.foo.yellow"',
            '"mypackage.foo.red"',
            '"mypackage.foo.blue" -> "mypackage.foo.green"',
            '"mypackage.foo.green" -> "mypackage.foo.yellow"',
            '"mypackage.foo.blue" -> "mypackage.foo.red"',
        }

    def _normalize_body(self, body: Iterable[str]) -> set[str]:
        return {item.strip() for item in body}
