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
@click.argument("module_name", type=str)
def drawgraph(module_name):
    use_cases.draw_graph(
        module_name=module_name,
        sys_path=sys.path,
        current_directory=os.getcwd(),
        build_graph=grimp.build_graph,
        viewer=adapters.RealGraphViewer(),
    )
