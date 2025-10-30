from textwrap import dedent
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Edge:
    source: str
    destination: str
    label: str

    def __str__(self) -> str:
        return f'"{DotGraph.render_module(self.source)}" ->  "{DotGraph.render_module(self.destination)}"{self._render_attrs()}\n'

    def _render_attrs(self) -> str:
        attrs: dict[str, str] = {}
        if self.label:
            attrs["label"] = self.label
        if attrs:
            joined_attrs = ", ".join([f'{key}="{value}"' for key, value in attrs.items()])
            return f" [{joined_attrs}]"
        else:
            return ""


class DotGraph:
    """
    A directed graph that can be rendered in DOT format.

    https://en.wikipedia.org/wiki/DOT_(graph_description_language)
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.nodes: set[str] = set()
        self.edges: set[Edge] = set()

    def add_node(self, name: str) -> None:
        self.nodes.add(name)

    def add_edge(self, edge: Edge) -> None:
        self.edges.add(edge)

    def render(self) -> str:
        # concentrate=true means that we merge the lines together.
        return dedent(f"""digraph {{
            node [fontname=helvetica]
            concentrate=true
            {self._render_nodes()}
            {self._render_edges()}
        }}""")

    def _render_nodes(self) -> str:
        return "\n".join(f'"{self.render_module(node)}"\n' for node in sorted(self.nodes))

    def _render_edges(self) -> str:
        return "\n".join(str(edge) for edge in sorted(self.edges))

    @staticmethod
    def render_module(module: str) -> str:
        # Render as relative module.
        return f".{module.split('.')[-1]}"
