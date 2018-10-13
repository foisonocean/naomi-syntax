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

from Naomi.system.paths import (
    SYNTAXES_BUILD_DIR,
    SYNTAXES_SRC_DIR,
)

from Naomi.system.compilers.syntaxes import compile_syntaxes
from sublime_plugin import ApplicationCommand


class NaomiBuildSyntaxesCommand(ApplicationCommand):
    def run(self):
        compile_syntaxes(
            SYNTAXES_SRC_DIR,
            SYNTAXES_BUILD_DIR,
        )
