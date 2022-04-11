"""
    TRS parsing output result
"""


class Tree(object):

    def __init__(self, root=None) -> None:
        self.cache = dict()
        self.root = root

        if self.root:
            self.root.post_processing()
            self.build_cache(self.root)

    def build_cache(self, root=None):
        if root:
            self.cache[root.index] = root

        for child in root.children:
            self.build_cache(child)

    def _remove_cache(self, root=None):
        if root:
            del self.cache[root.index]

        for child in root.children:
            self.build_cache(child)

    def clear_cache(self):
        self.cache.clear()

    def __str__(self):
        return str(self.root) + '\n'

    def __getitem__(self, item):
        return self.cache.get(item, None)

    def __setitem__(self, item, new_val):
        assert item in self.cache, 'Invalid position'
        assert isinstance(new_val, Tree) and new_val is not None, 'Not a valid Tree'

        new_val = new_val.root
        if item == '':
            self.clear_cache()
            self.root = new_val
            return

        # removing current node from cache
        self._remove_cache(self.__getitem__(item))

        parent_index, parent_child_index = item[:-1], int(item[-1]) - 1

        parent = self.__getitem__(parent_index)
        parent.children[parent_child_index] = new_val
        parent.reset_child_indices()
        parent.build_indices()
        self.build_cache(parent)


class TreeNode(object):

    def __init__(self, children=None, index='', value=None, is_variable=False):
        if children is None:
            children = []

        self.index = index
        self.value = value
        self.children = children
        self.is_variable = is_variable

    def __add__(self, other):
        assert isinstance(other, TreeNode), "Cannot __add__ TreeNode with something else"
        return [self, other]

    def __str__(self, level=0):
        out = ['\t'] * level
        out.append(f'TreeNode(value={self.value}; index=\'{self.index}\'; is_var={self.is_variable})')

        for child in self.children:
            out.append('\n' + child.__str__(level + 1))
        return ''.join(out)

    # To be called after building the syntax tree from the root node
    def post_processing(self):
        self.build_indices()

    def reset_child_indices(self):
        for child in self.children:
            child.index = ''
            child.reset_child_indices()

    def build_indices(self, parent_index=''):
        self.index += parent_index

        for i, child in enumerate(self.children):
            child.build_indices(self.index + str(i + 1))
