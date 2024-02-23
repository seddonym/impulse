import click
from .application import use_cases


@click.group()
def main():
    pass


@main.command()
@click.argument('module_name', type=str)
@click.option('--format', type=str, default='png')
def drawgraph(module_name, format):
    use_cases.draw_graph(
        module_name=module_name,
        file_format=format,
    )
