from collections.abc import Set
from typing import Callable
import itertools
import grimp
from impulse import ports, dotfile


def draw_graph(
    module_name: str,
    show_import_totals: bool,
    sys_path: list[str],
    current_directory: str,
    build_graph: Callable[[str], grimp.ImportGraph],
    viewer: ports.GraphViewer,
) -> None:
    """
    Create a file showing a graph of the supplied package.
    Args:
        module_name: the package or subpackage name of any importable Python package.
        show_import_totals: whether to label the arrows with the total number of imports they represent.
        sys_path: the sys.path list (or a test double).
        current_directory: the current working directory.
        build_graph: the function which builds the graph of the supplied package
            (pass grimp.build_graph or a test double).
        viewer: GraphViewer for generating the graph image and opening it.
    """
    # Add current directory to the path, as this doesn't happen automatically.
    sys_path.insert(0, current_directory)

    module = grimp.Module(module_name)
    grimp_graph = build_graph(module.package_name)

    dot = _build_dot(grimp_graph, module_name, show_import_totals)

    viewer.view(dot)


class _DotGraphBuildStrategy:
    def build(self, module_name: str, grimp_graph: grimp.ImportGraph) -> dotfile.DotGraph:
        children = grimp_graph.find_children(module_name)

        self.prepare_graph(grimp_graph, children)

        dot = dotfile.DotGraph(title=module_name)
        for child in children:
            dot.add_node(child)
        for upstream, downstream in itertools.permutations(children, r=2):
            if edge := self.build_edge(grimp_graph, upstream, downstream):
                dot.add_edge(edge)

        return dot

    def prepare_graph(self, grimp_graph: grimp.ImportGraph, children: Set[str]) -> None:
        pass

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        raise NotImplementedError


class _ModuleSquashingBuildStrategy(_DotGraphBuildStrategy):
    """Fast builder for when we don't need additional data about the imports."""

    def prepare_graph(self, grimp_graph: grimp.ImportGraph, children: Set[str]) -> None:
        for child in children:
            grimp_graph.squash_module(child)

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        if grimp_graph.direct_import_exists(importer=downstream, imported=upstream):
            return dotfile.Edge(source=downstream, destination=upstream)
        return None


class _ImportExpressionBuildStrategy(_DotGraphBuildStrategy):
    """Slower builder for when we want to work on the whole graph,
    without squashing children.
    """

    def __init__(self, show_import_totals: bool) -> None:
        self.show_import_totals = show_import_totals

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        if grimp_graph.direct_import_exists(
            importer=downstream, imported=upstream, as_packages=True
        ):
            if self.show_import_totals:
                number_of_imports = self._count_imports_between_packages(
                    grimp_graph, importer=downstream, imported=upstream
                )
                label = str(number_of_imports)
            else:
                label = ""
            return dotfile.Edge(source=downstream, destination=upstream, label=label)
        return None

    @staticmethod
    def _count_imports_between_packages(
        graph: grimp.ImportGraph, *, importer: str, imported: str
    ) -> int:
        return (
            len(graph.find_matching_direct_imports(import_expression=f"{importer} -> {imported}"))
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer} -> {imported}.**"
                )
            )
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer}.** -> {imported}"
                )
            )
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer}.** -> {imported}.**"
                )
            )
        )


def _build_dot(
    grimp_graph: grimp.ImportGraph,
    module_name: str,
    show_import_totals: bool,
) -> dotfile.DotGraph:
    strategy: _DotGraphBuildStrategy
    if show_import_totals:
        strategy = _ImportExpressionBuildStrategy(show_import_totals=True)
    else:
        strategy = _ModuleSquashingBuildStrategy()

    return strategy.build(module_name, grimp_graph)
