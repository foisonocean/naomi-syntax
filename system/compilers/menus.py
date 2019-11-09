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

from borela import (
    delete_dir_contents,
    list_files,
    load_yaml,
    to_json_string,
    write_text_file,
)

from Naomi.system import (
    EVENT_BUS,
    log_debug,
    log_info,
    package_relpath,
    STATE_STORE,
)

from Naomi.system.events import (
    building_menus,
    finished_building_menus,
)

from collections import defaultdict
from Naomi.system.headers import menu as menu_header
from os.path import join


def compile_menus():
    dir_path = STATE_STORE['directories']['integration']['menus']['src']
    dest_dir_path = (
        STATE_STORE['directories']['integration']['menus']['build']
    )

    EVENT_BUS.emit(building_menus())
    log_debug('Cleaning: %s' % package_relpath(dest_dir_path))

    delete_dir_contents(dest_dir_path)

    files = [file for file, _, _ in list_files(dir_path)]
    menus = load_menus(files)

    for location in menus:
        log_info('Building menus for %s...' % location)

        destination = join(dest_dir_path, '%s.sublime-menu' % location)
        final_string = menu_header() + to_json_string(
            menus[location],
            indent=True,
        )

        write_text_file(destination, final_string)
        log_debug('File generated: %s' % package_relpath(destination))

    log_info('Done building menus.')
    EVENT_BUS.emit(finished_building_menus())


def load_menus(files_paths):
    """
    Load all menu sources and returns the result indexed by the destination.
    """
    result = {}
    loaded_files = [
        load_menus_from_file(file_path)
        for file_path in files_paths
    ]

    for loaded_menus in loaded_files:
        # Files can be empty.
        if load_menus is None:
            continue

        for location in loaded_menus:
            if location not in result:
                result[location] = defaultdict(dict)
                result[location]['add'] = []
                result[location]['extend'] = []

            menus = loaded_menus[location]
            result[location]['add'].extend(menus.get('add', []))
            result[location]['extend'].extend(menus.get('extend', []))

    # Merge the result putting extensions first.
    merged_result = defaultdict(list)
    for location, menus in result.items():
        merged_result[location] = menus['extend'] + menus['add']

    return merged_result


def load_menus_from_file(file_path):
    """
    Load menus from a single source and returns the result indexed by
    destination.
    """

    relative_file_path = package_relpath(file_path)
    data = load_yaml(file_path)
    result = {}

    # Empty file.
    if data is None:
        log_debug('Empty file: %s' % relative_file_path)
        return None

    log_debug('Loading: %s' % relative_file_path)

    if 'location' not in data:
        message = 'Missing “location” for menu: %s' % relative_file_path
        raise ValueError(message)

    locations = data['location']

    # Single location.
    if isinstance(locations, str):
        locations = [locations]

    for location in locations:
        validate_location(location, file_path)
        if location not in result:
            result[location] = []
        result[location] = data['menus']

    log_debug('Done processing: %s' % relative_file_path)
    return result


def validate_location(location, file_path):
    valid_locations = [
        'Context',
        'Encoding',
        'Find in Files',
        'Indentation',
        'Line Endings',
        'Main',
        'Side Bar Mount Point',
        'Side Bar',
        'Syntax',
        'Tab Context',
        'Widget Context',
    ]

    if location not in valid_locations:
        message = 'Invalid location “%s” for file: %s' % (location, file_path)
        raise ValueError(message)
