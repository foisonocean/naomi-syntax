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
    Include,
    Resource,
)


def parse_include(syntax, context, raw):
    statement = Include()
    statement.syntax = syntax
    statement.context = context
    statement.raw = raw
    statement.path = raw['include']

    resource = Resource()
    resource.syntax = syntax
    resource.context = context
    resource.statement = statement
    resource.path = statement.path

    statement.resource = resource

    return statement