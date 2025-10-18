from textwrap import dedent


class DotGraph:
    """
    A directed graph that can be rendered in DOT format.

    https://en.wikipedia.org/wiki/DOT_(graph_description_language)
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.nodes: set[str] = set()
        self.edges: set[tuple[str, str, str]] = set()

    def add_node(self, name: str) -> None:
        self.nodes.add(name)

    def add_edge(self, *, source: str, destination: str, label: str) -> None:
        self.edges.add((source, destination, label))

    def render(self) -> str:
        # concentrate=true means that we merge the lines together.
        return dedent(f"""digraph {{
            node [fontname=helvetica]
            concentrate=true
            {self._render_nodes()}
            {self._render_edges()}
        }}""")

    def _render_nodes(self) -> str:
        return "\n".join(f'"{self._render_module(node)}"\n' for node in sorted(self.nodes))

    def _render_edges(self) -> str:
        return "\n".join(
            f'"{self._render_module(source)}" ->  "{self._render_module(destination)}"{self._render_label(label)}\n'
            for source, destination, label in sorted(self.edges)
        )

    def _render_module(self, module: str) -> str:
        return module.rsplit(self.title)[1]

    def _render_label(self, label: str) -> str:
        return f" [label={label}]" if label else ""
