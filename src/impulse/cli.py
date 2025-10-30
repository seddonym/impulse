import os

import click
import sys

from impulse.application import use_cases
from impulse import adapters
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
@click.argument("module_name", type=str)
def drawgraph(module_name: str, show_import_totals: bool, show_cycle_breakers: bool) -> None:
    use_cases.draw_graph(
        module_name=module_name,
        show_import_totals=show_import_totals,
        show_cycle_breakers=show_cycle_breakers,
        sys_path=sys.path,
        current_directory=os.getcwd(),
        build_graph=grimp.build_graph,
        viewer=adapters.BrowserGraphViewer(),
    )
