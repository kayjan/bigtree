def register_binarytree_plugins() -> None:
    """Register plugin for BinaryTree"""
    from bigtree.binarytree import construct
    from bigtree.binarytree.binarytree import BinaryTree
    from bigtree.utils import iterators

    binarytree_class_methods = {
        # Append methods
        "from_heapq_list": construct.list_to_binarytree,
    }
    binarytree_default_methods = {
        # Iterator methods
        "inorder_iter": iterators.inorder_iter,
    }
    BinaryTree.register_plugins(binarytree_class_methods, method="class")
    BinaryTree.register_plugins(binarytree_default_methods, method="default")

    plugin_docs = "\n".join(
        f"- `{name}()` — {getattr(func, '__doc__', '').splitlines()[0] if func.__doc__ else ''}"
        for name, func in BinaryTree._plugins.items()
    )
    BinaryTree.__doc__ = (
        BinaryTree.__doc__ or ""
    ) + f"\n\n## Registered Plugins\n\n{plugin_docs}"


def register_dag_plugins() -> None:
    """Register plugin for DAG"""
    from bigtree.dag import construct, export
    from bigtree.dag.dag import DAG
    from bigtree.utils import iterators

    dag_class_methods = {
        # Construct methods
        "from_dataframe": construct.dataframe_to_dag,
        "from_dict": construct.dict_to_dag,
        "from_list": construct.list_to_dag,
    }
    dag_default_methods = {
        # Export methods
        "to_dataframe": export.dag_to_dataframe,
        "to_dict": export.dag_to_dict,
        "to_list": export.dag_to_list,
        "to_dot": export.dag_to_dot,
        # Iterator methods
        "iterate": iterators.dag_iterator,
    }

    DAG.register_plugins(dag_class_methods, method="class")  # type: ignore[arg-type]
    DAG.register_plugins(dag_default_methods, method="default")  # type: ignore[arg-type]

    plugin_docs = "\n".join(
        f"- `{name}()` — {getattr(func, '__doc__', '').splitlines()[0] if func.__doc__ else ''}"
        for name, func in DAG._plugins.items()
    )
    DAG.__doc__ = (DAG.__doc__ or "") + f"\n\n## Registered Plugins\n\n{plugin_docs}"


def register_tree_plugins() -> None:
    """Register plugin for Tree"""
    from bigtree.tree import construct, export, helper, modify, query, search
    from bigtree.tree.tree import Tree
    from bigtree.utils import iterators

    tree_class_methods = {
        # Construct methods
        "from_dataframe": construct.dataframe_to_tree,
        "from_dataframe_relation": construct.dataframe_to_tree_by_relation,
        "from_polars": construct.polars_to_tree,
        "from_polars_relation": construct.polars_to_tree_by_relation,
        "from_dict": construct.dict_to_tree,
        "from_nested_dict": construct.nested_dict_to_tree,
        "from_nested_dict_key": construct.nested_dict_key_to_tree,
        "from_list": construct.list_to_tree,
        "from_list_relation": construct.list_to_tree_by_relation,
        "from_str": construct.str_to_tree,
        "from_newick": construct.newick_to_tree,
        "from_rich": construct.rich_to_tree,
    }
    tree_default_methods = {
        # Append methods
        "add_dataframe_by_path": construct.add_dataframe_to_tree_by_path,
        "add_dataframe_by_name": construct.add_dataframe_to_tree_by_name,
        "add_polars_by_path": construct.add_polars_to_tree_by_path,
        "add_polars_by_name": construct.add_polars_to_tree_by_name,
        "add_dict_by_path": construct.add_dict_to_tree_by_path,
        "add_dict_by_name": construct.add_dict_to_tree_by_name,
        # Export methods
        "show": export.print_tree,
        "hshow": export.hprint_tree,
        "vshow": export.vprint_tree,
        "ishow": export.iprint_tree,
        "yield_tree": export.yield_tree,
        "hyield": export.hyield_tree,
        "vyield": export.vyield_tree,
        "to_dataframe": export.tree_to_dataframe,
        "to_polars": export.tree_to_polars,
        "to_dict": export.tree_to_dict,
        "to_nested_dict": export.tree_to_nested_dict,
        "to_nested_dict_key": export.tree_to_nested_dict_key,
        "to_html": export.tree_to_html,
        "to_newick": export.tree_to_newick,
        "to_dot": export.tree_to_dot,
        "to_pillow_graph": export.tree_to_pillow_graph,
        "to_pillow": export.tree_to_pillow,
        "to_mermaid": export.tree_to_mermaid,
        "to_vis": export.tree_to_vis,
        # Iterator methods
        "preorder_iter": iterators.preorder_iter,
        "postorder_iter": iterators.postorder_iter,
        "levelorder_iter": iterators.levelorder_iter,
        "levelordergroup_iter": iterators.levelordergroup_iter,
        "zigzag_iter": iterators.zigzag_iter,
        "zigzaggroup_iter": iterators.zigzaggroup_iter,
        # Modify methods
        "shift_nodes": modify.shift_nodes,
        "copy_nodes": modify.copy_nodes,
        "shift_and_replace_nodes": modify.shift_and_replace_nodes,
        # Query methods
        "query": query.query_tree,
        # Search methods
        "findall": search.findall,
        "find": search.find,
        "find_name": search.find_name,
        "find_names": search.find_names,
        "find_relative_path": search.find_relative_path,
        "find_relative_paths": search.find_relative_paths,
        "find_full_path": search.find_full_path,
        "find_path": search.find_path,
        "find_paths": search.find_paths,
        "find_attr": search.find_attr,
        "find_attrs": search.find_attrs,
        "find_children": search.find_children,
        "find_child": search.find_child,
        "find_child_by_name": search.find_child_by_name,
    }
    tree_helper_methods = {
        # Helper methods
        "clone": helper.clone_tree,
        "subtree": helper.get_subtree,
        "prune": helper.prune_tree,
    }
    tree_diff_methods = {
        # Helper methods
        "diff_dataframe": helper.get_tree_diff_dataframe,
        "diff": helper.get_tree_diff,
    }

    Tree.register_plugins(tree_class_methods, method="class")  # type: ignore[arg-type]
    Tree.register_plugins(tree_default_methods, method="default")  # type: ignore[arg-type]
    Tree.register_plugins(tree_helper_methods, method="helper")  # type: ignore[arg-type]
    Tree.register_plugins(tree_diff_methods, method="diff")

    plugin_docs = "\n".join(
        f"- `{name}()` — {getattr(func, '__doc__', '').splitlines()[0] if func.__doc__ else ''}"
        for name, func in Tree._plugins.items()
    )
    Tree.__doc__ = (Tree.__doc__ or "") + f"\n\n## Registered Plugins\n\n{plugin_docs}"
