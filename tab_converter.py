bottom_string = 'E'

octave1 = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
octave2 = ["e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#"]
octave3 = ["e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "b'", "c'", "c#'", "d'", "d#'"]

all_notes = octave1 + octave2 + octave3

# Ellie's standard octave, maybe octave up from standard guitar octave
dulcimer_map = {
    "E": "[1]",
    "G": "[2]",
    "A": "[3]",
    "B": "[4]",
    "C": "[5]",
    "C#": "1",
    "D": "[6]/2",
    "D#": "3",
    "e": "[7]",
    "f": "[8]",
    "f#": "4",
    "g": "5",
    "g#": "[9]/(1)",
    "a": "[10]/6/(2)",
    "a#": "[11]/(3)",
    "b": "[12]/7",
    "c": "8",
    "c#": "(4)",
    "d": "9/(5)",
    "d#": "10",
    "e'": "(6)",
    "f'": "11",
    "f#'": "(7)",
    "g'": "(8)",
    "g#'": "12",
    "a'": "(9)",
    "a#'": "(10)",
    "c'": "(11)",
    "d#'": "(12)",
}


def parse_tab_lines(lines):
    tab_lines = []
    tab_line = {}

    for line in lines:
        line.replace('h', '-')
        line.replace('p', '-')

        if line.endswith('|\n') or line.endswith('|'):

            tab_line[line[0]] = line[1::].strip('\n')

            if line.startswith(bottom_string):
                tab_lines.append(tab_line)

                tab_line = {}

    return tab_lines


def parse_tab_file(tab_file_path):
    """
    Loads a file of

    :param tab_file_path:
    :return:
    """
    with open(tab_file_path) as tab:
        return parse_tab_lines(tab.readlines())


def parse_tab_string(tab_string, delim='\n'):
    return parse_tab_lines(tab_string.split(delim))


def extract_frets(guitar_string):
    frets = {}
    bar_lines = {}

    for i in range(1, len(guitar_string) - 1):
        if ' ' == guitar_string[i - 1]:
            continue

        if (guitar_string[i] + guitar_string[i + 1]).isnumeric():
            frets[i] = int(guitar_string[i] + guitar_string[i + 1])

        elif guitar_string[i].isnumeric() and not guitar_string[i - 1].isnumeric():
            frets[i] = int(guitar_string[i])

        elif guitar_string[i] == '|':
            bar_lines[i] = '|'

    return frets, bar_lines


def fret_to_note(string_name, fret_number):
    i = all_notes.index(string_name)
    return all_notes[i + fret_number]


def frets_to_notes(string_name, frets):
    notes = {}
    for beat in frets:
        notes[beat] = fret_to_note(string_name, frets[beat])

    return notes


def place_notes_in_beat_order(notes, bar_lines=None):
    """

    :param bar_lines:
    :type notes: dict
    """
    if bar_lines is None:
        bar_lines = {}

    phrase = ''

    last_beat = max(notes)

    for beat in range(0, last_beat + 1):
        if beat in notes:
            phrase = phrase + notes[beat]
        else:
            if beat in bar_lines:
                phrase = phrase + '|'
            else:
                phrase = phrase + '-'

    return phrase


def notes_to_dulcimer_tab(notes, last_beat, bar_lines=None):
    if bar_lines is None:
        bar_lines = {}

    dulcimer_tab = ''

    unit_width = 0
    for note in dulcimer_map:
        if len(dulcimer_map[note]) > unit_width:
            unit_width = len(dulcimer_map[note])

    for beat in range(0, last_beat + 1):
        if beat in notes:
            if notes[beat] in dulcimer_map:
                fill_value = dulcimer_map[notes[beat]]
            else:
                fill_value = notes[beat]

            padded_fill_value = fill_value + '-' * (unit_width - len(fill_value))

            dulcimer_tab = dulcimer_tab + padded_fill_value

        elif beat in bar_lines:
            dulcimer_tab = dulcimer_tab + '|' * unit_width

        else:
            dulcimer_tab = dulcimer_tab + '-' * unit_width

    return dulcimer_tab


def tab_line_to_notes(tab_line):
    notes = {}
    all_bar_lines = {}

    for string_name in tab_line:
        frets, bar_lines = extract_frets(guitar_string=tab_line[string_name])

        all_bar_lines.update(bar_lines)
        notes.update(frets_to_notes(string_name=string_name, frets=frets))

    return notes, all_bar_lines


def guitar_tab_lines_to_dulcimer(tab_lines):
    dulcimer_tab = ''

    for tab_line in tab_lines:
        notes, bar_lines = tab_line_to_notes(tab_line)
        dulcimer_tab += notes_to_dulcimer_tab(notes, len(tab_line['e']), bar_lines) + '\n\n'

    return dulcimer_tab


def main():
    with open('tab.txt') as tab_file:
        guitar_tab_string = tab_file.read()

    # guitar_tab_lines = parse_tab_file('tab.txt')
    guitar_tab_lines = parse_tab_string(guitar_tab_string)

    dulcimer_tab = guitar_tab_lines_to_dulcimer(guitar_tab_lines)
    print(dulcimer_tab)


def guitar_to_dulcimer_tab(request):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json()
    if request_json and 'tab' in request_json:
        tab_string = request_json['tab']
    else:
        return 'No guitar tab passed in', 200, headers

    dulcimer_tab = guitar_tab_lines_to_dulcimer(parse_tab_string(tab_string))

    return dulcimer_tab, 200, headers


if __name__ == '__main__':
    main()
