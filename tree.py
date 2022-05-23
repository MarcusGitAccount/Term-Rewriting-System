"""
    TRS parsing output result

    Check page 36 of the textbook

    TODO:
    - position comparison
    - term reduction
    - ackermann function
"""
from __future__ import annotations

from copy import deepcopy
from random import shuffle


def print_mapping(mapping):
    for k, v in mapping.items():
        print(f'{k} -> {str(v)}')


class Tree(object):
    LOGGER = {
        False: lambda *args, **kwargs: None,  # no operation
        True: print
    }

    def __init__(self, root=None, signature=None) -> None:
        self.cache = dict()
        self.root = root

        if self.root:
            self._init()

    def _init(self):
        self.root.index = ''
        self.root.reset_child_indices()
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
                self._remove_cache(child)

    def copy(self):
        """Returns a deep copy of current tree"""
        return deepcopy(self)

    def _clear_cache(self):
        self.cache.clear()

    def is_instance_from(self, s):
        """
            Checks if self >= s (self is an instance of s)
            Checks whether current term is an instance of @param s.
            If it is return the substitution mapping used
        """

        assert isinstance(s, Tree), "Not a valid term"
        false_none = False, None

        # step 1: assert all non-terminal nodes in @s and @self are equal(holding the same symbol)
        # curr_non_vars = self.get_non_variable_positions()
        s_non_vars = s.get_non_variable_positions()

        # print(curr_non_vars)
        # print(s_non_vars)
        for pos in s_non_vars:
            if self[pos].value != s[pos].value:
                return false_none

        # step 2: assert all variable positions in @s are valid positions in @self
        # step 3: based on the previous step check there exists a substitution mapping @s -> @self

        s_vars = s.get_variable_positions()
        mapping = {}
        for pos in s_vars:
            val = s[pos].value
            sub = self.__getitem__(index_position=pos, get_as_tree=True)
            if val not in mapping:
                mapping[val] = sub
            elif mapping[val] != sub:
                return false_none

        return True, mapping

    def reduction(self, sigma_identities, new_tree=False, verbose=False):
        """
            Tries to perform a reduction over the identities given
        """

        shuffle(sigma_identities)
        for index, (lhs, rhs) in enumerate(sigma_identities):
            # Given every non-variable position in the left-hand side of the
            # identity check if @self is an instance of the sub-term at that
            # position
            non_var_pos = self.cache.keys()
            for pos in non_var_pos:
                # subterm = lhs.__getitem__(index_position=pos, get_as_tree=True)
                curr_subterm = self.__getitem__(index_position=pos, get_as_tree=True)
                is_mapping, mapping = curr_subterm.is_instance_from(lhs)

                if is_mapping:
                    Tree.LOGGER[verbose](
                        f'Found suitable reduction with identity {str(lhs)} ~ {str(rhs)} at position \'{pos}\'')

                    if verbose:
                        print_mapping(mapping)

                    Tree.LOGGER[verbose](f'Applying found substitution to rhs')
                    new = rhs.substitute_variables(mapping, new_tree=True)

                    Tree.LOGGER[verbose](f'Replacing in current term at \'{pos}\' with previous result')
                    term = self.copy() if new_tree else self
                    term[pos] = new
                    return term
        return self

    def substitute_variables(self, substitutions, new_tree=False):
        """
            Substitution of variable nodes
            @new_tree = True -> creates a copy of the tree
        """
        if new_tree:
            return self.copy().substitute_variables(substitutions, new_tree=False)

        var_positions = self.get_variable_positions()

        for var_pos in var_positions:
            curr = self.cache[var_pos].value
            if curr not in substitutions:
                continue
            new_val = substitutions[curr]
            self[var_pos] = deepcopy(new_val)
        return self

    def get_positions(self):
        """Pos(t) - get set of positions for current term t"""
        return list(self.cache.keys())

    def get_variables(self):
        """Var(t) - set of variables occurring in current term t"""
        return {node.value for pos, node in self.cache.items() if node.is_variable}

    def get_variable_positions(self):
        return {pos for pos, node in self.cache.items() if node.is_variable}

    def get_non_variable_positions(self):
        return {pos for pos, node in self.cache.items() if not node.is_variable}

    # Compare positions

    # Parallel positions

    def __eq__(self, other):
        if not isinstance(other, Tree):
            return False
        return self.root == other.root

    def __neq__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        """|s| - cardinality of term(i.e. number of nodes in the syntax tree)"""
        return len(self.cache)

    def __repr__(self):
        return repr(self.root) + '\n'

    def __str__(self):
        return str(self.root)

    def __getitem__(self, index_position: str, get_as_tree=False):
        """
            Get position
            @param get_as_tree: if True, will create a wrapper Tree over the requested node at position @item
        """
        node = self.cache.get(index_position, None)
        if not get_as_tree:
            return node
        return Tree(deepcopy(node))

    def __setitem__(self, index_position: str, new_val) -> None:
        """Replacement at position @index_position with term @new_val"""
        assert index_position in self.cache, 'Invalid position'
        assert isinstance(new_val, Tree) and new_val is not None, 'Not a valid Tree'

        new_val = new_val.root
        if index_position == '':
            # Root node, we can delete the whole cache since it's faster than replacing it
            self._clear_cache()
            self.root = new_val
            self._init()
            return

        # removing current node from cache

        parent_index, parent_child_index = index_position[:-1], int(index_position[-1]) - 1

        self._remove_cache(self.__getitem__(index_position))
        parent = self.__getitem__(parent_index)
        parent.children[parent_child_index] = new_val

        parent.reset_child_indices()
        parent.build_indices()
        self.build_cache(parent)
        # print(repr(self))


class TreeNode(object):

    def __init__(self, children=None, index='', value=None, is_variable=False, arity=0):
        if children is None:
            children = []

        self.arity = arity
        self.index = index
        self.value = value
        self.children = children
        self.is_variable = is_variable

    def __add__(self, other):
        assert isinstance(other, TreeNode), "Cannot __add__ TreeNode with something else"
        return [self, other]

    def __repr__(self, level=0):
        out = ['\t'] * level
        out.append(f'TreeNode(value={self.value}; '
                   f'index=\'{self.index}\'; '
                   f'is_var={self.is_variable}; '
                   f'arity={self.arity})')

        for child in self.children:
            out.append('\n' + child.__repr__(level + 1))
        return ''.join(out)

    def __str__(self):
        if self.is_variable or self.arity == 0:
            return self.value
        children = [str(child) for child in self.children]
        return f'{self.value}({", ".join(children)})'

    # It's enough to compare the symbol held recursively. Internal state doesn't matter when it comes to equality
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        if self.value != other.value:
            return False
        if len(self.children) != len(other.children):
            return False
        for a, b in zip(self.children, other.children):
            if not a.__eq__(b):
                return False
        return True

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


class TreeNodeIndex(object):
    def __init__(self, value):
        self._val = value

    def __repr__(self):
        return self._val

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if not isinstance(other, TreeNodeIndex):
            return False
        return self._val == other._val

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)
