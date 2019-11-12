# Licensed under the Apache License, Version 2.0 (the “License”); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


def word_list_to_word_binary_tree(words):
    if all([len(word) == 1 for word in words]):
        return words

    node = {
        'root': '',
        'left': [],
        'right': [],
    }

    character = words[0][:1]

    if character:
        node['root'] += character

        for word in words:
            if word.startswith(character):
                node['left'].append(word[1:])
            else:
                node['right'].append(word)
    else:
        node['right'] = words[1:]

    node['left'] = word_list_to_word_binary_tree(node['left'])
    node['right'] = word_list_to_word_binary_tree(node['right'])

    return node


def word_binary_tree_to_string(node):
    root = node['root']
    left = node['left']
    right = node['right']

    left_pattern = ''
    if isinstance(left, list):
        if len(left) > 0:
            left_pattern = '(?>%s)' % '|'.join(left)
    else:
        left_pattern = word_binary_tree_to_string(left)

    if len(right) < 1:
        return root + left_pattern

    right_pattern = word_binary_tree_to_string(right)

    if not left_pattern:
        return '(?:%s%s)?' % (root, right_pattern)

    return '(?>%s%s|%s)' % (root, left_pattern, right_pattern)


def make_words_regex(words):
    """
    Transforms a list of words into an optimized regex, for example:

        foo
        bar
        baz
        foobar
        foobaz

    becomes:

        \b(?>ba(?>r|z)|foo(?:ba(?>r|z))?)\b
    """
    # Sorting is not necessary but it will be easier to debug.
    words.sort()
    # This will turn the words into a binary tree and extract the root that
    # connect each group of words.
    tree = word_list_to_word_binary_tree(words)
    # Build the optimized regex.
    result = word_binary_tree_to_string(tree)
    # Add a word boundary to to prevent partial matches.
    return '\\b%s\\b' % result