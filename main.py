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


def read_tab_file(tab_file_path):
    with open(tab_file_path) as tab:

        tab_lines = []

        tab_line = {}
        for line in tab.readlines():
            line.replace('h', '-')
            line.replace('p', '-')

            if line.endswith('|\n') or line.endswith('|'):

                tab_line[line[0]] = line[1::].strip('\n')

                if line[0] == bottom_string:
                    tab_lines.append(tab_line)

                    tab_line = {}

        return tab_lines


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
    """

    :type notes: dict
    """
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


def main():
    tab_lines = read_tab_file('tab.txt')

    for tab_line in tab_lines:
        notes, bar_lines = tab_line_to_notes(tab_line)
        print(notes_to_dulcimer_tab(notes, len(tab_line['e']), bar_lines), '\n')


if __name__ == '__main__':
    main()
