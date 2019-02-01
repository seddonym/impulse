import click
from .application import use_cases


@click.group()
def main():
    pass


@main.command()
@click.argument('module_name', type=str)
def drawgraph(module_name):
    use_cases.draw_graph(
        module_name=module_name,
    )
