import os

import click
import sys

from impulse.application import use_cases
from impulse import adapters
from impulse import ports
import grimp


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--show-import-totals",
    is_flag=True,
    help="Label arrows with the number of imports they represent.",
)
@click.option(
    "--show-cycle-breakers",
    is_flag=True,
    help=(
        "Identify a set of dependencies that, if removed, would make the graph acyclic, "
        "and display them as dashed lines."
    ),
)
@click.option(
    "--format",
    type=click.Choice(["html", "dot"]),
    default="html",
    help="Output format (default to html).",
)
@click.option("--force-console", is_flag=True, help="Force the use of the console output.")
@click.option(
    "--hide-unlinked",
    is_flag=True,
    help="Hide nodes that have no incoming or outgoing edges.",
)
@click.option(
    "--hide-nodes",
    type=str,
    default="",
    help=(
        "Comma-separated list of fnmatch patterns to hide nodes. "
        "Patterns are matched against relative module names (without leading dot). "
        "Example: --hide-nodes=foo,bar.* hides .foo, .bar.plop, .bar.plip.plup"
    ),
)
@click.option(
    "--depth",
    type=int,
    default=1,
    help="Depth of submodules to include in the graph (default: 1 for direct children).",
)
@click.argument("module_name", type=str)
def drawgraph(
    module_name: str,
    show_import_totals: bool,
    show_cycle_breakers: bool,
    force_console: bool,
    format: str,
    hide_unlinked: bool,
    hide_nodes: str,
    depth: int,
) -> None:
    # Parse hide_nodes patterns (comma-separated list)
    hide_nodes_patterns = (
        [p.strip() for p in hide_nodes.split(",") if p.strip()] if hide_nodes else []
    )

    viewer: ports.GraphViewer
    if format == "html":
        if not force_console and sys.stdout.isatty():
            # the output is not redirected to a file
            viewer = adapters.BrowserGraphViewer()
        else:
            viewer = adapters.ConsoleGraphViewer()
    elif format == "dot":
        viewer = adapters.ConsoleDotViewer()
    else:
        raise ValueError(f"Invalid format: {format}")
    use_cases.draw_graph(
        module_name=module_name,
        show_import_totals=show_import_totals,
        show_cycle_breakers=show_cycle_breakers,
        hide_unlinked=hide_unlinked,
        hide_nodes_patterns=hide_nodes_patterns,
        depth=depth,
        sys_path=sys.path,
        current_directory=os.getcwd(),
        get_top_level_package=adapters.get_top_level_package,
        build_graph=grimp.build_graph,
        viewer=viewer,
    )
