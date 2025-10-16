import graphviz


class GraphViewer:
    """
    Abstraction for generating the graph image and opening it using the default os viewer.
    """

    def view(self, dot: graphviz.Digraph) -> None:
        raise NotImplementedError
