'''
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>

---------------------------------------------------------------------

The Software provides no guarantee of any accuracy when searching for
individuals. The Software relies solely on one source to gather this
information, and should not be used to make any type of decision.

A name alone does not identify an individual.
'''

import re
import sys
import requests


def get_names(state, city):
    matches = []

    # download list of names
    try:
        req = requests.get('https://mugshots.com/US-States/{0}/{1}/'.format(state, city), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        if req.status_code != 200:
            print("[ERROR] (get_names): server returned NON OK on request")
            return False

        matches = re.findall(r'''<div class="label">([a-z0-1\. ]+)</div>''', req.text, re.I)
        if len(matches) == 0:
            print("[WARNING] (get_names): could not fetch any names from website")
            return False
    except Exception as e:
        print("[ERROR] (get_names): "+str(e))
        return False

    # remove middle innitials and convert to upper case
    for i, name in enumerate(matches):
        name = name.upper()
        split = name.split(' ')
        if len(split) == 2: matches[i] = name
        else: matches[i] = split[0]+' '+split[2]

    return matches


def search_names(names):
    stored = []

    try:
        with open('names.txt', 'r') as f:
            for line in f:
                line = line.strip()

                if len(line) == 0: continue
                stored.append(line)
    except Exception as e:
        print("[ERROR] (search_names): "+str(e))
        return

    for name in stored:
        if name in names: print("Found: " + name)


def main():
    names = []

    if len(sys.argv) != 3:
        print("MugSearch, a python tool to automatically search through arrest records to determine if a name exists in them.\n\n"+
              "Usage: python main.py STATE COUNTY\n\n"+
              "Notes:\n"+
              "\tUse https://mugshots.com/US-States/ to browse available states and counties.\n"+
              "\tWrite in the names you wish to find in 'names.txt' in full capitals.\n"+
              "\t\t- First and last name only. One name per line. The file contains examples.\n\n"+
              "Examples:\n"+
              "\tpython main.py Utah Summit-County-UT\n"+
              "\tpython main.py Tennessee Clay-County-TN")
        return
    else: names = get_names(sys.argv[1], sys.argv[2])
    if names is False: return

    search_names(names)


if __name__ == '__main__':
    main()
