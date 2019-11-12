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

from .ast import (
    FunctionCall,
    Match,
    Pop,
)

from .parse_pop import parse_pop
from .parse_push import parse_push
from .parse_set import parse_set
from .ParsingError import ParsingError
from borela.functions import make_words_regex
from collections import OrderedDict


def dict_to_function_calls(calls):
    result = []
    for name, args in calls.items():
        result.append(FunctionCall(name, args))
    return result


def parse_match(syntax, context, raw):
    statement = Match()
    statement.syntax = syntax
    statement.context = context
    statement.raw = raw

    for i, (key, value) in enumerate(raw.items(), 1):
        if key == 'match':
            # Literal pattern.
            if isinstance(value, (bool, str, float, int)):
                statement.pattern = str(value)
                continue

            # Function calls.
            if isinstance(value, (list, OrderedDict)) and len(value) > 0:
                nodes = []

                # Simple function calls.
                if isinstance(value, OrderedDict):
                    nodes = dict_to_function_calls(value)
                # Function calls mixed with literals.
                else:
                    for item in value:
                        if isinstance(item, str):
                            nodes.append(item)
                            continue

                        if isinstance(item, OrderedDict):
                            nodes.extend(dict_to_function_calls(item))

                if len(nodes) > 1:
                    nodes = FunctionCall('join', nodes)

                statement.pattern = nodes
                continue

            raise ParsingError(
                '(%i, %i) Unsupported statement or expression.' % (
                raw.lc.line + i,
                raw.lc.col,
            ))

        if key == 'match_word':
            statement.pattern = FunctionCall('word', value)
            continue

        if key == 'match_words':
            statement.pattern = FunctionCall('words', value)
            continue

        if key == 'scope':
            statement.scope = value
            continue

        if key == 'captures':
            statement.captures = value
            continue

        if key == 'with_prototype':
            statement.with_prototype = value
            continue

        if key in ['push', 'set', 'pop']:
            if statement.stack_action:
                raise ParsingError(
                    '(%i, %i) Multiple stack control statements.' % (
                    raw.lc.line + i,
                    raw.lc.col,
                ))

            if key == 'push':
                statement.stack_action = parse_push(
                    syntax,
                    context,
                    value,
                )
                continue

            if key == 'set':
                statement.stack_action = parse_set(
                    syntax,
                    context,
                    value,
                )
                continue

            if key == 'pop':
                statement.stack_action = parse_pop(
                    syntax,
                    context,
                    value,
                )
                continue

        raise ParsingError('(%i, %i) Unexpected statement: %s' % (
            raw.lc.line + i,
            raw.lc.col,
            key,
        ))

    return statement