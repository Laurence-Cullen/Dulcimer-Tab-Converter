bottom_string = 'E'

octave1 = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
octave2 = ["e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#"]
octave3 = ["e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "b'", "c'", "c#'", "d'", "d#'"]

all_notes = octave1 + octave2 + octave3


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

    for i in range(1, len(guitar_string) - 1):
        if (guitar_string[i] + guitar_string[i + 1]).isnumeric():
            frets[i] = int(guitar_string[i] + guitar_string[i + 1])

        elif guitar_string[i].isnumeric() and not guitar_string[i - 1].isnumeric():
            frets[i] = int(guitar_string[i])

    return frets


def fret_to_note(string_name, fret_number):
    i = all_notes.index(string_name)
    return all_notes[i + fret_number]


def frets_to_notes(string_name, frets):
    notes = {}
    for beat in frets:
        notes[beat] = fret_to_note(string_name, frets[beat])

    return notes


def place_notes_in_beat_order(notes):
    """

    :type notes: dict
    """
    phrase = ''

    last_beat = max(notes)

    for beat in range(0, last_beat + 1):
        if beat in notes:
            phrase = phrase + notes[beat]
        else:
            phrase = phrase + '-'

    return phrase


def tab_line_to_phrase(tab_line):
    notes = {}

    for string_name in tab_line:
        frets = extract_frets(guitar_string=tab_line[string_name])

        notes.update(frets_to_notes(string_name=string_name, frets=frets))

    phrase = place_notes_in_beat_order(notes)

    return phrase


def main():
    tab_lines = read_tab_file('tab.txt')

    for tab_line in tab_lines:
        print(tab_line_to_phrase(tab_line))


if __name__ == '__main__':
    main()

