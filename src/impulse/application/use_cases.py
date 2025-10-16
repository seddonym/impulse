from typing import Callable
import itertools
import grimp
from impulse import ports
from graphviz import Digraph


def draw_graph(
    module_name: str,
    sys_path: list[str],
    current_directory: str,
    build_graph: Callable[[str], grimp.ImportGraph],
    viewer: ports.GraphViewer,
) -> None:
    """
    Create a file showing a graph of the supplied package.
    Args:
        module_name: the package or subpackage name of any importable Python package.
        sys_path: the sys.path list (or a test double).
        current_directory: the current working directory.
        build_graph: the function which builds the graph of the supplied package
            (pass grimp.build_graph or a test double).
        viewer: GraphViewer for generating the graph image and opening it.
    """
    # Add current directory to the path, as this doesn't happen automatically.
    sys_path.insert(0, current_directory)

    module = grimp.Module(module_name)
    graph = build_graph(module.package_name)
    module_children = graph.find_children(module.name)

    dot = Digraph(format="png", node_attr={"fontname": "helvetica"})
    dot.attr(
        concentrate="true",  # Merge lines together.
    )
    for module_child in module_children:
        dot.node(module_child)

    # Dependencies between children.
    for upstream, downstream in itertools.permutations(module_children, r=2):
        if graph.direct_import_exists(imported=upstream, importer=downstream, as_packages=True):
            dot.edge(downstream, upstream)

    viewer.view(dot)
