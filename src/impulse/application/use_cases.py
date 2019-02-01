import itertools
import tempfile
import sys
import os

from graphviz import Digraph  # type: ignore
import grimp  # type: ignore


def draw_graph(module_name: str) -> None:
    """
    Create a file showing a graph of the supplied package.
    Args:
        module_name: the package or subpackage name of any importable Python package.
    """
    # Add current directory to the path, as this doesn't happen automatically.
    sys.path.insert(0, os.getcwd())

    module = grimp.Module(module_name)
    graph = grimp.build_graph(module.package_name)
    module_children = graph.find_children(module.name)

    dot = Digraph(
        format='png',
        node_attr={'fontname': 'helvetica'}
    )
    dot.attr(
        concentrate='true',  # Merge lines together.
    )
    for module_child in module_children:
        dot.node(module_child)

    # Dependencies between children.
    for upstream, downstream in itertools.permutations(module_children, r=2):
        if graph.direct_import_exists(
                imported=upstream, importer=downstream, as_packages=True):
            dot.edge(downstream, upstream)

    source_filename = tempfile.mkstemp()[1]
    dot.view(filename=source_filename, cleanup=True)
