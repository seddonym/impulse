from impulse.application import use_cases
from copy import copy
from impulse import dotfile
from impulse.dotfile import Edge
import grimp
from impulse import ports

SOME_ROOT_PACKAGE = "mypackage"
SOME_MODULE = f"{SOME_ROOT_PACKAGE}.foo"


def fake_get_top_level_package_non_namespace(module_name: str) -> str:
    return module_name.split(".")[0]


def build_fake_graph(package_name: str) -> grimp.ImportGraph:
    graph = grimp.ImportGraph()
    graph.add_module(package_name)

    graph.add_module(SOME_MODULE)

    for child in ("blue", "green", "yellow", "red"):
        graph.add_module(f"{SOME_MODULE}.{child}")

    graph.add_import(
        importer=f"{SOME_MODULE}.blue.alpha",
        imported=f"{SOME_MODULE}.green",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.green",
        imported=f"{SOME_MODULE}.yellow.beta",
    )
    # Add 4 imports between blue and red in different permutations of root and descendants.
    graph.add_import(
        importer=f"{SOME_MODULE}.blue",
        imported=f"{SOME_MODULE}.red",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.blue",
        imported=f"{SOME_MODULE}.red.gamma",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.blue.alpha",
        imported=f"{SOME_MODULE}.red",
    )
    graph.add_import(
        importer=f"{SOME_MODULE}.blue.delta",
        imported=f"{SOME_MODULE}.red.epsilon",
    )
    # Add a cycle.
    graph.add_import(
        importer=f"{SOME_MODULE}.red.epsilon",
        imported=f"{SOME_MODULE}.blue.alpha",
    )

    return graph


class SpyGraphViewer(ports.GraphViewer):
    def __init__(self) -> None:
        self.called_with_dot: dotfile.DotGraph | None = None

    def view(self, dot: dotfile.DotGraph) -> None:
        self.called_with_dot = dot


class TestDrawGraph:
    def test_draw_graph(self):
        original_sys_path = ["/some/path", "/another/path"]
        sys_path = copy(original_sys_path)
        current_directory = "/cwd"
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=sys_path,
            current_directory=current_directory,
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
        )

        # The current directory was added to system path.
        assert sys_path == [current_directory, *original_sys_path]
        # The image generation function was called.
        assert viewer.called_with_dot, "Viewer not called."
        assert viewer.called_with_dot.title == SOME_MODULE
        assert viewer.called_with_dot.concentrate is True
        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.green",
            "mypackage.foo.blue",
            "mypackage.foo.yellow",
            "mypackage.foo.red",
        }
        assert viewer.called_with_dot.edges == {
            Edge("mypackage.foo.blue", "mypackage.foo.green"),
            Edge("mypackage.foo.green", "mypackage.foo.yellow"),
            Edge("mypackage.foo.blue", "mypackage.foo.red"),
            Edge("mypackage.foo.red", "mypackage.foo.blue"),
        }

    def test_draw_graph_calls_top_level_package(self):
        def get_top_level_package(module: str) -> str:
            return "some.namespace"

        def asserting_build_graph(top_level_package: str) -> grimp.ImportGraph:
            assert top_level_package == "some.namespace"
            graph = grimp.ImportGraph()
            graph.add_module("some.namespace")
            graph.add_module("some.namespace.foo")
            graph.add_module("some.namespace.foo.blue")
            graph.add_module("some.namespace.foo.blue.alpha")
            graph.add_module("some.namespace.foo.blue.beta")
            return graph

        viewer = SpyGraphViewer()
        use_cases.draw_graph(
            "some.namespace.foo.blue",
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=get_top_level_package,
            build_graph=asserting_build_graph,
            viewer=viewer,
        )

    def test_draw_graph_show_import_totals(self):
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=True,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
        )

        assert viewer.called_with_dot.concentrate is False
        assert viewer.called_with_dot.edges == {
            Edge("mypackage.foo.blue", "mypackage.foo.green", label="1"),
            Edge("mypackage.foo.green", "mypackage.foo.yellow", label="1"),
            Edge("mypackage.foo.blue", "mypackage.foo.red", label="4"),
            Edge("mypackage.foo.red", "mypackage.foo.blue", label="1"),
        }

    def test_draw_graph_show_cycle_breakers(self):
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=True,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
        )

        assert viewer.called_with_dot.concentrate is False
        assert viewer.called_with_dot.edges == {
            Edge(
                "mypackage.foo.blue",
                "mypackage.foo.green",
            ),
            Edge(
                "mypackage.foo.green",
                "mypackage.foo.yellow",
            ),
            Edge(
                "mypackage.foo.blue",
                "mypackage.foo.red",
            ),
            Edge("mypackage.foo.red", "mypackage.foo.blue", emphasized=True),
        }

    def test_draw_graph_depth_2(self):
        """Test that depth=2 shows children AND grandchildren of the module."""

        def build_graph_with_depth(package_name: str) -> grimp.ImportGraph:
            graph = grimp.ImportGraph()
            graph.add_module(package_name)
            graph.add_module(SOME_MODULE)

            # Create a hierarchy: foo.blue, foo.green, foo.blue.alpha, foo.blue.beta, foo.green.gamma
            for child in ("blue", "green"):
                graph.add_module(f"{SOME_MODULE}.{child}")
            for grandchild in ("alpha", "beta"):
                graph.add_module(f"{SOME_MODULE}.blue.{grandchild}")
            graph.add_module(f"{SOME_MODULE}.green.gamma")

            # Add imports at the grandchild level
            graph.add_import(
                importer=f"{SOME_MODULE}.blue.alpha",
                imported=f"{SOME_MODULE}.green.gamma",
            )
            graph.add_import(
                importer=f"{SOME_MODULE}.blue.beta",
                imported=f"{SOME_MODULE}.green.gamma",
            )
            # Add import at the child level
            graph.add_import(
                importer=f"{SOME_MODULE}.blue",
                imported=f"{SOME_MODULE}.green",
            )
            return graph

        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_graph_with_depth,
            viewer=viewer,
            depth=2,
        )

        assert viewer.called_with_dot.depth == 2
        # depth=2 includes both children (depth 1) AND grandchildren (depth 2)
        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.blue",
            "mypackage.foo.green",
            "mypackage.foo.blue.alpha",
            "mypackage.foo.blue.beta",
            "mypackage.foo.green.gamma",
        }
        assert viewer.called_with_dot.edges == {
            Edge("mypackage.foo.blue", "mypackage.foo.green"),
            Edge("mypackage.foo.blue.alpha", "mypackage.foo.green.gamma"),
            Edge("mypackage.foo.blue.beta", "mypackage.foo.green.gamma"),
        }
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 39624fc (hide unlinked)

    def test_draw_graph_hide_unlinked(self):
        """Test that hide_unlinked=True removes nodes with no edges."""
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
            hide_unlinked=True,
        )

        # The default graph has blue, green, yellow, red nodes
        # yellow has no direct edges (only green -> yellow), but it IS connected
        # All four nodes are connected in the test graph, so all should remain
        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.green",
            "mypackage.foo.blue",
            "mypackage.foo.yellow",
            "mypackage.foo.red",
        }

    def test_draw_graph_hide_unlinked_removes_isolated_nodes(self):
        """Test that hide_unlinked=True removes truly isolated nodes."""

        def build_graph_with_isolated(package_name: str) -> grimp.ImportGraph:
            graph = grimp.ImportGraph()
            graph.add_module(package_name)
            graph.add_module(SOME_MODULE)

            # Create some children, one of which is isolated
            for child in ("blue", "green", "isolated"):
                graph.add_module(f"{SOME_MODULE}.{child}")

            # Only blue and green are connected
            graph.add_import(
                importer=f"{SOME_MODULE}.blue",
                imported=f"{SOME_MODULE}.green",
            )
            # "isolated" has no imports
            return graph

        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_graph_with_isolated,
            viewer=viewer,
            hide_unlinked=True,
        )

        # Only blue and green should remain; isolated should be filtered out
        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.blue",
            "mypackage.foo.green",
        }
        assert viewer.called_with_dot.edges == {
            Edge("mypackage.foo.blue", "mypackage.foo.green"),
        }
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6e23bb0 (depth)
=======
>>>>>>> 39624fc (hide unlinked)
=======

    def test_draw_graph_hide_nodes_exact_match(self):
        """Test that hide_nodes_patterns hides exact matching nodes."""
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
            hide_nodes_patterns=["blue"],
        )

        # "blue" should be hidden, but "blue.alpha" etc. should NOT be hidden
        # since the pattern "blue" only matches exactly "blue"
        assert "mypackage.foo.blue" not in viewer.called_with_dot.nodes
        assert "mypackage.foo.green" in viewer.called_with_dot.nodes
        assert "mypackage.foo.yellow" in viewer.called_with_dot.nodes
        assert "mypackage.foo.red" in viewer.called_with_dot.nodes

    def test_draw_graph_hide_nodes_wildcard_pattern(self):
        """Test that hide_nodes_patterns with wildcard hides matching nodes."""

        def build_graph_for_wildcard(package_name: str) -> grimp.ImportGraph:
            graph = grimp.ImportGraph()
            graph.add_module(package_name)
            graph.add_module(SOME_MODULE)

            # Create a hierarchy to test wildcard patterns
            for child in ("foo", "bar", "baz", "other"):
                graph.add_module(f"{SOME_MODULE}.{child}")

            graph.add_import(
                importer=f"{SOME_MODULE}.foo",
                imported=f"{SOME_MODULE}.other",
            )
            return graph

        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_graph_for_wildcard,
            viewer=viewer,
            hide_nodes_patterns=["ba*"],  # Should hide "bar" and "baz"
        )

        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.foo",
            "mypackage.foo.other",
        }

    def test_draw_graph_hide_nodes_nested_wildcard(self):
        """Test that hide_nodes_patterns with nested wildcard hides matching nodes."""

        def build_graph_for_nested(package_name: str) -> grimp.ImportGraph:
            graph = grimp.ImportGraph()
            graph.add_module(package_name)
            graph.add_module(SOME_MODULE)

            # Create depth 2 hierarchy
            for child in ("bar", "other"):
                graph.add_module(f"{SOME_MODULE}.{child}")
            for grandchild in ("plop", "plip"):
                graph.add_module(f"{SOME_MODULE}.bar.{grandchild}")
            graph.add_module(f"{SOME_MODULE}.other.thing")

            graph.add_import(
                importer=f"{SOME_MODULE}.bar.plop",
                imported=f"{SOME_MODULE}.other.thing",
            )
            return graph

        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_graph_for_nested,
            viewer=viewer,
            depth=2,
            hide_nodes_patterns=["bar.*"],  # Should hide "bar.plop" and "bar.plip"
        )

        # bar.plop and bar.plip should be hidden
        assert "mypackage.foo.bar.plop" not in viewer.called_with_dot.nodes
        assert "mypackage.foo.bar.plip" not in viewer.called_with_dot.nodes
        # bar and other.thing should remain
        assert "mypackage.foo.bar" in viewer.called_with_dot.nodes
        assert "mypackage.foo.other" in viewer.called_with_dot.nodes
        assert "mypackage.foo.other.thing" in viewer.called_with_dot.nodes

    def test_draw_graph_hide_nodes_multiple_patterns(self):
        """Test that multiple hide_nodes_patterns work together."""
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
            hide_nodes_patterns=["blue", "red"],  # Hide both blue and red
        )

        assert viewer.called_with_dot.nodes == {
            "mypackage.foo.green",
            "mypackage.foo.yellow",
        }

    def test_draw_graph_hide_nodes_removes_corresponding_edges(self):
        """Test that hiding nodes also removes edges to/from those nodes."""
        viewer = SpyGraphViewer()

        use_cases.draw_graph(
            SOME_MODULE,
            show_import_totals=False,
            show_cycle_breakers=False,
            sys_path=[],
            current_directory="/cwd",
            get_top_level_package=fake_get_top_level_package_non_namespace,
            build_graph=build_fake_graph,
            viewer=viewer,
            hide_nodes_patterns=["blue"],
        )

        # Edges involving blue should be gone
        for edge in viewer.called_with_dot.edges:
            assert "blue" not in edge.source
            assert "blue" not in edge.destination
>>>>>>> cbfc506 (hide nodes)
