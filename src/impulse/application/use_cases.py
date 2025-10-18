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
    graph = build_graph(module.package_name)
    module_children = graph.find_children(module.name)

    dot = dotfile.DotGraph(title=module_name)

    for module_child in module_children:
        dot.add_node(module_child)

    # Dependencies between children.
    for upstream, downstream in itertools.permutations(module_children, r=2):
        if graph.direct_import_exists(importer=downstream, imported=upstream, as_packages=True):
            if show_import_totals:
                number_of_imports = _count_imports_between_packages(
                    graph, importer=downstream, imported=upstream
                )
                label = str(number_of_imports)
            else:
                label = ""
            dot.add_edge(source=downstream, destination=upstream, label=label)
    viewer.view(dot)


def _count_imports_between_packages(
    graph: grimp.ImportGraph, *, importer: str, imported: str
) -> int:
    return (
        len(graph.find_matching_direct_imports(import_expression=f"{importer} -> {imported}"))
        + len(graph.find_matching_direct_imports(import_expression=f"{importer} -> {imported}.**"))
        + len(graph.find_matching_direct_imports(import_expression=f"{importer}.** -> {imported}"))
        + len(
            graph.find_matching_direct_imports(import_expression=f"{importer}.** -> {imported}.**")
        )
    )
