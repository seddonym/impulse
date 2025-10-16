import graphviz
import tempfile
from impulse import ports


class RealGraphViewer(ports.GraphViewer):
    """
    Graph viewer that generates an image as a temporary file and opens it in a popup.
    """

    def view(self, dot: graphviz.Digraph) -> None:
        source_filename = tempfile.mkstemp()[1]
        dot.view(filename=source_filename, cleanup=True)
