bottom_string = 'E'

octave0 = ["Eb"]
octave1 = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
octave2 = ["e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#"]
octave3 = ["e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "b'", "c'", "c#'", "d'", "d#'"]
octave4 = ["e''", "f''", "f#''", "g''", "g#''", "a''", "a#''", "b''", "c''", "c#''", "d''", "d#''"]


all_notes = octave0 + octave1 + octave2 + octave3 + octave4

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
    string_notes = []

    for line in lines:
        line.replace('h', '-')
        line.replace('p', '-')

        if line.endswith('|\n') or line.endswith('|'):

            string_note = line.split('|')[0]
            string_note = normalise_note(string_note)

            tab_line[string_note] = line[len(string_note)::].strip('\n')
            string_notes.append(string_note)

            if line.startswith(bottom_string):

                tab_line = rationalise_tab_line(tab_line, string_notes)

                tab_lines.append(tab_line)

                tab_line = {}

    return tab_lines


def rationalise_tab_line(tab_line, notes):
    """Rationalise notes in tab line, start from bottom string note assuming
    that is accurate, then iterate up through notes determining the actual
    notes they map to.

    Return a tab_line with fixed keys.
    """
    rationalised_tab_line = {}
    rationalised_notes = []

    # reverse order of notes so that the first note is the bottom string
    bot_up_notes = notes[::-1]

    previous_note = bot_up_notes[0]

    # print('notes:', notes)

    for note in bot_up_notes:
        if note.startswith(bottom_string):
            rationalised_tab_line[note] = tab_line[note]
            rationalised_notes.append(note)
            continue

        # print('note to rationalise:', note)

        for i in range(all_notes.index(previous_note) + 1, len(all_notes)):
            candidate_note = all_notes[i]

            # print('candidate note:', candidate_note)

            if note.lower() == candidate_note.replace("'", "").lower():
                # print(note, 'matched with', candidate_note)
                rationalised_tab_line[candidate_note] = tab_line[note]
                rationalised_notes.append(candidate_note)
                previous_note = candidate_note
                break

    return rationalised_tab_line


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


def fret_to_note(string_name, fret_number, semitone_transpose):

    # print(string_name)
    # print(fret_number)

    i = all_notes.index(string_name)

    return all_notes[i + fret_number + semitone_transpose]


def frets_to_notes(string_name, frets, semitone_transpose):
    notes = {}
    for beat in frets:
        notes[beat] = fret_to_note(string_name, frets[beat], semitone_transpose=semitone_transpose)

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


def tab_line_to_notes(tab_line, semitone_transpose):
    notes = {}
    all_bar_lines = {}

    for string_name in tab_line:
        frets, bar_lines = extract_frets(guitar_string=tab_line[string_name])

        all_bar_lines.update(bar_lines)
        notes.update(frets_to_notes(string_name=string_name, frets=frets, semitone_transpose=semitone_transpose))

    return notes, all_bar_lines


def guitar_tab_lines_to_dulcimer(tab_lines, semitone_transpose=0):
    dulcimer_tab = ''

    for tab_line in tab_lines:
        notes, bar_lines = tab_line_to_notes(tab_line, semitone_transpose=semitone_transpose)
        # print(tab_line)
        dulcimer_tab += notes_to_dulcimer_tab(notes, len(list(tab_line.values())[0]), bar_lines) + '\n\n'

    return dulcimer_tab


def normalise_note(note):

    if len(note) == 1:
        return note
    elif len(note) == 2:

        if note[1] == 'b':
            transpose = -1
        elif note[1] == '#':
            transpose = 1
        else:
            raise ValueError('invalid note modifier:', note[1])

        return all_notes[all_notes.index(note[0]) + transpose]
    else:
        raise ValueError('note length error, length =', len(note))


def main():
    with open('bright_side.txt') as tab_file:
        guitar_tab_string = tab_file.read()

    # guitar_tab_lines = parse_tab_file('tab.txt')
    guitar_tab_lines = parse_tab_string(guitar_tab_string)

    # print(guitar_tab_lines)

    dulcimer_tab = guitar_tab_lines_to_dulcimer(guitar_tab_lines, semitone_transpose=-12)
    print(dulcimer_tab)

    # for key in list(dulcimer_tab.keys()):
    #     print(key, dulcimer_tab[key])


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
        semitone_transpose = int(request_json['semitoneTranspose'])
    else:
        return 'No guitar tab passed in', 200, headers

    dulcimer_tab = guitar_tab_lines_to_dulcimer(parse_tab_string(tab_string), semitone_transpose=semitone_transpose)

    return dulcimer_tab, 200, headers


if __name__ == '__main__':
    main()
