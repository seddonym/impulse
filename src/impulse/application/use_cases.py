from collections.abc import Set
from collections.abc import Callable
import fnmatch
import itertools
import grimp
from impulse import ports, dotfile


def draw_graph(
    module_name: str,
    show_import_totals: bool,
    show_cycle_breakers: bool,
    sys_path: list[str],
    current_directory: str,
    get_top_level_package: Callable[[str], str],
    build_graph: Callable[[str], grimp.ImportGraph],
    viewer: ports.GraphViewer,
    depth: int = 1,
<<<<<<< HEAD
<<<<<<< HEAD
    hide_unlinked: bool = False,
<<<<<<< HEAD
=======
>>>>>>> 6e23bb0 (depth)
=======
    hide_unlinked: bool = False,
>>>>>>> 39624fc (hide unlinked)
=======
    hide_nodes_patterns: list[str] | None = None,
>>>>>>> cbfc506 (hide nodes)
) -> None:
    """
    Create a file showing a graph of the supplied package.
    Args:
        module_name: the package or subpackage name of any importable Python package.
        show_import_totals: whether to label the arrows with the total number of imports they represent.
        show_cycle_breakers: marks a set of dependencies that, if removed, would make the graph acyclic.
        sys_path: the sys.path list (or a test double).
        current_directory: the current working directory.
        get_top_level_package: the function to retrieve the top level package name. This will usually be the first part
            of the dotted module name (before the first dot), but for namespace packages it should be the 'portion' name.
        build_graph: the function which builds the graph of the supplied package
            (pass grimp.build_graph or a test double).
        viewer: GraphViewer for generating the graph image and opening it.
        depth: the depth of submodules to include in the graph (default: 1 for direct children).
<<<<<<< HEAD
<<<<<<< HEAD
        hide_unlinked: whether to hide nodes that have no incoming or outgoing edges.
<<<<<<< HEAD
=======
>>>>>>> 6e23bb0 (depth)
=======
        hide_unlinked: whether to hide nodes that have no incoming or outgoing edges.
>>>>>>> 39624fc (hide unlinked)
=======
        hide_nodes_patterns: list of fnmatch patterns to hide matching nodes.
>>>>>>> cbfc506 (hide nodes)
    """
    # Add current directory to the path, as this doesn't happen automatically.
    sys_path.insert(0, current_directory)

    top_level_package = get_top_level_package(module_name)
    grimp_graph = build_graph(top_level_package)

<<<<<<< HEAD
<<<<<<< HEAD
    dot = _build_dot(
        grimp_graph, module_name, show_import_totals, show_cycle_breakers, depth, hide_unlinked,
        hide_nodes_patterns=hide_nodes_patterns or [],
    )
=======
    dot = _build_dot(grimp_graph, module_name, show_import_totals, show_cycle_breakers, depth)
>>>>>>> 6e23bb0 (depth)
=======
    dot = _build_dot(
        grimp_graph, module_name, show_import_totals, show_cycle_breakers, depth, hide_unlinked
    )
>>>>>>> 39624fc (hide unlinked)

    viewer.view(dot)


def _find_modules_up_to_depth(
    grimp_graph: grimp.ImportGraph, module_name: str, depth: int
) -> Set[str]:
    """
    Find all modules up to and including the specified depth below the given module.

    For depth=1, returns direct children.
    For depth=2, returns direct children AND grandchildren.
    And so on.
    """
    if depth < 1:
        raise ValueError("Depth must be at least 1")

    all_modules: set[str] = set()
    current_level = {module_name}

    for _ in range(depth):
        next_level: set[str] = set()
        for mod in current_level:
            next_level.update(grimp_graph.find_children(mod))
        all_modules.update(next_level)
        current_level = next_level

    return all_modules


def _should_hide_node(module: str, base_module: str, patterns: list[str]) -> bool:
    """
    Check if a module should be hidden based on fnmatch patterns.

    Patterns are matched against the relative module name (without leading dot).
    For example, if base_module is "mypackage.foo" and module is "mypackage.foo.bar.baz",
    the relative name is "bar.baz" and patterns like "bar" or "bar.*" are matched against it.
    """
    if not patterns:
        return False

    # Get the relative module name (strip the base module prefix)
    if module.startswith(base_module + "."):
        relative = module[len(base_module) + 1:]  # Strip base module and the dot
    else:
        # Fallback: use just the last component
        relative = module.split(".")[-1]

    # Check if any pattern matches
    for pattern in patterns:
        if fnmatch.fnmatch(relative, pattern):
            return True

    return False


class _DotGraphBuildStrategy:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, depth: int = 1, hide_unlinked: bool = False) -> None:
        self.depth = depth
        self.hide_unlinked = hide_unlinked
=======
    def __init__(self, depth: int = 1) -> None:
        self.depth = depth
>>>>>>> 6e23bb0 (depth)
=======
    def __init__(self, depth: int = 1, hide_unlinked: bool = False) -> None:
        self.depth = depth
        self.hide_unlinked = hide_unlinked
>>>>>>> 39624fc (hide unlinked)
=======
    def __init__(self, depth: int = 1, hide_unlinked: bool = False, hide_nodes_patterns: list[str] | None = None) -> None:
        self.depth = depth
        self.hide_unlinked = hide_unlinked
        self.hide_nodes_patterns = hide_nodes_patterns or []
>>>>>>> cbfc506 (hide nodes)

    def build(self, module_name: str, grimp_graph: grimp.ImportGraph) -> dotfile.DotGraph:
        modules = _find_modules_up_to_depth(grimp_graph, module_name, self.depth)

        # Filter out hidden nodes based on patterns
        if self.hide_nodes_patterns:
            modules = {
                mod for mod in modules
                if not _should_hide_node(mod, module_name, self.hide_nodes_patterns)
            }

        self.prepare_graph(grimp_graph, modules)

        dot = dotfile.DotGraph(
            title=module_name, concentrate=self.should_concentrate(), depth=self.depth
        )
<<<<<<< HEAD
<<<<<<< HEAD

        # Build edges first so we can determine which nodes are linked
        edges: list[dotfile.Edge] = []
=======
        for mod in modules:
            dot.add_node(mod)
>>>>>>> 6e23bb0 (depth)
=======

        # Build edges first so we can determine which nodes are linked
        edges: list[dotfile.Edge] = []
>>>>>>> 39624fc (hide unlinked)
        for upstream, downstream in itertools.permutations(modules, r=2):
            if edge := self.build_edge(grimp_graph, upstream, downstream):
                edges.append(edge)

        # Determine which nodes have at least one connection
        if self.hide_unlinked:
            linked_nodes: set[str] = set()
            for edge in edges:
                linked_nodes.add(edge.source)
                linked_nodes.add(edge.destination)
            nodes_to_add = modules & linked_nodes
        else:
            nodes_to_add = modules

        for mod in nodes_to_add:
            dot.add_node(mod)
        for edge in edges:
            dot.add_edge(edge)

        return dot

    def should_concentrate(self) -> bool:
        return True

    def prepare_graph(self, grimp_graph: grimp.ImportGraph, modules: Set[str]) -> None:
        pass

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        raise NotImplementedError


class _ModuleSquashingBuildStrategy(_DotGraphBuildStrategy):
    """Fast builder for when we don't need additional data about the imports."""

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, depth: int = 1, hide_unlinked: bool = False) -> None:
        super().__init__(depth=depth, hide_unlinked=hide_unlinked)
=======
    def __init__(self, depth: int = 1, hide_unlinked: bool = False, hide_nodes_patterns: list[str] | None = None) -> None:
        super().__init__(depth=depth, hide_unlinked=hide_unlinked, hide_nodes_patterns=hide_nodes_patterns)
>>>>>>> cbfc506 (hide nodes)

=======
>>>>>>> 6e23bb0 (depth)
=======
    def __init__(self, depth: int = 1, hide_unlinked: bool = False) -> None:
        super().__init__(depth=depth, hide_unlinked=hide_unlinked)

>>>>>>> 39624fc (hide unlinked)
    def prepare_graph(self, grimp_graph: grimp.ImportGraph, modules: Set[str]) -> None:
        for mod in modules:
            grimp_graph.squash_module(mod)

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        if grimp_graph.direct_import_exists(importer=downstream, imported=upstream):
            return dotfile.Edge(source=downstream, destination=upstream)
        return None


class _ImportExpressionBuildStrategy(_DotGraphBuildStrategy):
    """Slower builder for when we want to work on the whole graph,
    without squashing modules.
    """

    def __init__(
        self,
        *,
        module_name: str,
        show_import_totals: bool,
        show_cycle_breakers: bool,
        depth: int = 1,
<<<<<<< HEAD
<<<<<<< HEAD
        hide_unlinked: bool = False,
        hide_nodes_patterns: list[str] | None = None,
    ) -> None:
<<<<<<< HEAD
        super().__init__(depth=depth, hide_unlinked=hide_unlinked)
=======
    ) -> None:
        super().__init__(depth=depth)
>>>>>>> 6e23bb0 (depth)
=======
        hide_unlinked: bool = False,
    ) -> None:
        super().__init__(depth=depth, hide_unlinked=hide_unlinked)
>>>>>>> 39624fc (hide unlinked)
=======
        super().__init__(depth=depth, hide_unlinked=hide_unlinked, hide_nodes_patterns=hide_nodes_patterns)
>>>>>>> cbfc506 (hide nodes)
        self.module_name = module_name
        self.show_import_totals = show_import_totals
        self.show_cycle_breakers = show_cycle_breakers
        self.cycle_breakers: set[tuple[str, str]] | None = None

    def should_concentrate(self) -> bool:
        # We need to see edge direction emphasized separately.
        return not (self.show_import_totals or self.show_cycle_breakers)

    def prepare_graph(self, grimp_graph: grimp.ImportGraph, modules: Set[str]) -> None:
        super().prepare_graph(grimp_graph, modules)

        if self.show_cycle_breakers:
            self.cycle_breakers = self._get_coarse_grained_cycle_breakers(grimp_graph, modules)

    def _get_coarse_grained_cycle_breakers(
        self, grimp_graph: grimp.ImportGraph, modules: Set[str]
    ) -> set[tuple[str, str]]:
        # In the form (importer, imported).
        coarse_grained_cycle_breakers: set[tuple[str, str]] = set()

        for fine_grained_cycle_breaker in grimp_graph.nominate_cycle_breakers(self.module_name):
            importer, imported = fine_grained_cycle_breaker
            importer_ancestor = self._get_self_or_ancestor(candidate=importer, ancestors=modules)
            imported_ancestor = self._get_self_or_ancestor(candidate=imported, ancestors=modules)

            if importer_ancestor and imported_ancestor:
                coarse_grained_cycle_breakers.add((importer_ancestor, imported_ancestor))

        return coarse_grained_cycle_breakers

    @staticmethod
    def _get_self_or_ancestor(candidate: str, ancestors: Set[str]) -> str | None:
        for ancestor in ancestors:
            if candidate == ancestor or candidate.startswith(f"{ancestor}."):
                return ancestor
        return None

    def build_edge(
        self, grimp_graph: grimp.ImportGraph, upstream: str, downstream: str
    ) -> dotfile.Edge | None:
        # For depth > 1, we can't use as_packages=True because modules may share
        # descendants (e.g., foo.blue and foo.blue.alpha are both in our set).
        # In that case, only check for direct imports between exact modules.
        if self.depth > 1:
            import_exists = grimp_graph.direct_import_exists(
                importer=downstream, imported=upstream, as_packages=False
            )
        else:
            import_exists = grimp_graph.direct_import_exists(
                importer=downstream, imported=upstream, as_packages=True
            )

        if import_exists:
            if self.show_import_totals:
                number_of_imports = self._count_imports_between_packages(
                    grimp_graph, importer=downstream, imported=upstream
                )
                label = str(number_of_imports)
            else:
                label = ""

            if self.show_cycle_breakers:
                assert self.cycle_breakers is not None
                is_cycle_breaker = (downstream, upstream) in self.cycle_breakers
                emphasized = is_cycle_breaker
            else:
                emphasized = False

            return dotfile.Edge(
                source=downstream, destination=upstream, label=label, emphasized=emphasized
            )
        return None

    @staticmethod
    def _count_imports_between_packages(
        graph: grimp.ImportGraph, *, importer: str, imported: str
    ) -> int:
        return (
            len(graph.find_matching_direct_imports(import_expression=f"{importer} -> {imported}"))
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer} -> {imported}.**"
                )
            )
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer}.** -> {imported}"
                )
            )
            + len(
                graph.find_matching_direct_imports(
                    import_expression=f"{importer}.** -> {imported}.**"
                )
            )
        )


def _build_dot(
    grimp_graph: grimp.ImportGraph,
    module_name: str,
    show_import_totals: bool,
    show_cycle_breakers: bool,
    depth: int = 1,
<<<<<<< HEAD
<<<<<<< HEAD
    hide_unlinked: bool = False,
<<<<<<< HEAD
=======
>>>>>>> 6e23bb0 (depth)
=======
    hide_unlinked: bool = False,
>>>>>>> 39624fc (hide unlinked)
=======
    hide_nodes_patterns: list[str] | None = None,
>>>>>>> cbfc506 (hide nodes)
) -> dotfile.DotGraph:
    strategy: _DotGraphBuildStrategy
    # Use ImportExpressionBuildStrategy when:
    # - show_import_totals or show_cycle_breakers is enabled, OR
    # - depth > 1 (squashing would remove deeper modules we want to show)
    if show_import_totals or show_cycle_breakers or depth > 1:
        strategy = _ImportExpressionBuildStrategy(
            module_name=module_name,
            show_import_totals=show_import_totals,
            show_cycle_breakers=show_cycle_breakers,
            depth=depth,
<<<<<<< HEAD
<<<<<<< HEAD
            hide_unlinked=hide_unlinked,
            hide_nodes_patterns=hide_nodes_patterns,
        )
    else:
<<<<<<< HEAD
        strategy = _ModuleSquashingBuildStrategy(depth=depth, hide_unlinked=hide_unlinked)
=======
        )
    else:
        strategy = _ModuleSquashingBuildStrategy(depth=depth)
>>>>>>> 6e23bb0 (depth)
=======
            hide_unlinked=hide_unlinked,
        )
    else:
        strategy = _ModuleSquashingBuildStrategy(depth=depth, hide_unlinked=hide_unlinked)
>>>>>>> 39624fc (hide unlinked)
=======
        strategy = _ModuleSquashingBuildStrategy(depth=depth, hide_unlinked=hide_unlinked, hide_nodes_patterns=hide_nodes_patterns)
>>>>>>> cbfc506 (hide nodes)

    return strategy.build(module_name, grimp_graph)
