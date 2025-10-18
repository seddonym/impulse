from impulse import dotfile


class GraphViewer:
    """
    Abstraction for rendering and displaying a graph visualization.
    """

    def view(self, dot: dotfile.DotGraph) -> None:
        raise NotImplementedError
