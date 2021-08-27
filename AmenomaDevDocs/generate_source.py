from io import TextIOWrapper
import os
import sys


class Tree:
    def __init__(self) -> None:
        self.parent = None
        self.children = {}
        self.var = ""


def write_markdown_recursive(tree: Tree, prefix: str, file: TextIOWrapper, layer: int) -> None:
    if tree == None:
        return

    # indent
    for i in range(layer):
        file.write("  ")

    name = tree.var[:-3] if tree.var.endswith(".md") else tree.var

    file.write("* [" + name + "](" +
               os.path.join(prefix, name + ".md") + ")\n")

    for key, value in tree.children.items():
        if value == None:
            continue
        new_prefix = os.path.join(prefix, tree.var)
        write_markdown_recursive(value, new_prefix, file, layer + 1)


def write_markdown(tree: Tree, file: TextIOWrapper, prefix: str) -> None:
    file.write("# " + tree.var + "\n\n")
    write_markdown_recursive(tree, prefix, file, 0)


def recursive_traverse_dir(dir: str) -> Tree:
    if not os.path.isdir(dir):
        tree = Tree()
        tree.var = os.path.basename(dir)
        print(tree.var)
        return tree

    file_list = os.listdir(dir)
    tree = Tree()
    tree.var = os.path.basename(dir)

    for file in file_list:
        full_path = os.path.join(dir, file)
        child_node = recursive_traverse_dir(full_path)
        tree.children[child_node.var] = child_node

    print(tree.var)
    # write_markdown(tree, dir)
    return tree


def write_source_tree(tree: Tree, dir: str, prefix: str):
    if tree == None:
        return
    if not tree.children:
        return

    file = open(os.path.join(dir, tree.var + ".md"), "w")
    write_markdown(tree, file, prefix)
    file.close()
    for key, value in tree.children.items():
        write_source_tree(value, os.path.join(dir, tree.var),
                          os.path.join(prefix, tree.var))


if __name__ == "__main__":
    base_dir = sys.argv[1]
    source_dir = os.path.join(base_dir, "source")
    tree = recursive_traverse_dir(source_dir)

    for key, value in tree.children.items():
        son = value
        if son.children:
            write_source_tree(son, source_dir, os.path.join("/source"))

    side_bar = open(os.path.join(base_dir, "_sidebar.md"), "a")
    for key, value in tree.children.items():
        son = value
        if son.children:
            write_markdown_recursive(son, "/source", side_bar, 1)

    side_bar.close()
