import pathlib

import flask
import midi

bottom_string = 'E'

octave0 = ["Eb"]
octave1 = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
octave2 = ["e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#"]
octave3 = ["e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "b'", "c'", "c#'", "d'", "d#'"]
octave4 = ["e''", "f''", "f#''", "g''", "g#''", "a''", "a#''", "b''", "c''", "c#''", "d''", "d#''"]

all_notes = octave0 + octave1 + octave2 + octave3 + octave4
pitch_to_note = {
    99: "d#''",
    98: "d''",
    97: "c#''",
    96: "c''",
    95: "b''",
    94: "a#''",
    93: "a''",
    92: "g#''",
    91: "g''",
    90: "f#''",
    89: "f''",
    88: "e''",
    87: "d#'",
    86: "d'",
    85: "c#'",
    84: "c'",
    83: "b'",
    82: "a#'",
    81: "a'",
    80: "g#'",
    79: "g'",
    78: "f#'",
    77: "f'",
    76: "e'",
    75: "d#",
    74: "d",
    73: "c#",
    72: "c",
    71: "b",
    70: "a#",
    69: "a",
    68: "g#",
    67: "g",
    66: "f#",
    65: "f",
    64: "e",
    63: "D#",
    62: "D",
    61: "C#",
    60: "C",
    59: "B",
    58: "A#",
    57: "A",
    56: "G#",
    55: "G",
    54: "F#",
    53: "F",
    52: "E",
    51: "Eb"
}


def note_from_pitch(pitch: int) -> str:
    try:
        return pitch_to_note[pitch]
    except KeyError:
        raise KeyError(
            f"MIDI pitch {pitch} is outside of supported range "
            f"{min(pitch_to_note.keys())} - {max(pitch_to_note.keys())}"
        )


# Ellie's standard octave, maybe octave up from standard guitar octave
note_to_dulcimer_string = {
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


def get_midi_pitches(file_path: str):
    song = midi.read_midifile(file_path)
    song.make_ticks_abs()

    if len(song) > 1:
        raise ValueError(f"The MIDI file contains {len(song)} tracks, the maximum is 1.")
    track = song[0]

    note_ons = []
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            note_ons.append(event)

    pitches = {}
    for note in note_ons:
        if note.tick in pitches:
            pitches[note.tick].append(note.pitch)
        else:
            pitches[note.tick] = [note.pitch]

    return pitches


def parse_tab_lines(lines: list):
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

        for i in range(notes.index(previous_note) + 1, len(notes)):
            candidate_note = notes[i]

            # print('candidate note:', candidate_note)

            if note.lower() == candidate_note.replace("'", "").lower():
                # print(note, 'matched with', candidate_note)
                rationalised_tab_line[candidate_note] = tab_line[note]
                rationalised_notes.append(candidate_note)
                previous_note = candidate_note
                break

    return rationalised_tab_line


def parse_tab_file(tab_file_path):
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
    i = all_notes.index(string_name)
    return all_notes[i + fret_number + semitone_transpose]


def frets_to_notes(string_name, frets, semitone_transpose):
    notes = {}
    for beat in frets:
        notes[beat] = fret_to_note(string_name, frets[beat], semitone_transpose=semitone_transpose)

    return notes


def transpose_note(note: str, semitone_transpose: int):
    note_index = all_notes.index(note)
    return all_notes[note_index + semitone_transpose]


def place_notes_in_beat_order(notes: dict, bar_lines=None):
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


def get_unit_width():
    unit_width = 0
    for note in note_to_dulcimer_string:
        if len(note_to_dulcimer_string[note]) > unit_width:
            unit_width = len(note_to_dulcimer_string[note])

    return unit_width


def validate_fill_char(fill_char: str):
    if len(fill_char) != 1:
        raise ValueError(f"fill char must be a string of length 1, got length: {len(fill_char)}")


def note_to_dulc_tab_string(note: str, unit_width: int, fill_char: str = '-'):
    validate_fill_char(fill_char)
    fill_value = note_to_dulcimer_string.get(note, note)
    return fill_value + fill_char * (unit_width - len(fill_value))


def empty_dulc_tab_string(unit_width: int, fill_char: str = '-'):
    validate_fill_char(fill_char)
    return fill_char * unit_width


def notes_to_dulcimer_tab(notes, last_beat: int, bar_lines=None):
    if bar_lines is None:
        bar_lines = {}

    dulcimer_tab = ''

    unit_width = get_unit_width()

    for beat in range(0, last_beat + 1):
        if beat in notes:
            dulcimer_tab += note_to_dulc_tab_string(notes[beat], unit_width)
        elif beat in bar_lines:
            dulcimer_tab = dulcimer_tab + '|' * unit_width
        else:
            dulcimer_tab = dulcimer_tab + '-' * unit_width

    return dulcimer_tab


def tab_line_to_notes(tab_line, semitone_transpose: int):
    notes = {}
    all_bar_lines = {}

    for string_name in tab_line:
        frets, bar_lines = extract_frets(guitar_string=tab_line[string_name])

        all_bar_lines.update(bar_lines)
        notes.update(frets_to_notes(string_name=string_name, frets=frets, semitone_transpose=semitone_transpose))

    return notes, all_bar_lines


def guitar_tab_lines_to_dulcimer(tab_lines: list, semitone_transpose: int = 0):
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


def max_concurrent_notes(pitches: dict) -> int:
    return max([len(pitches_at_tick) for pitches_at_tick in pitches.values()])


def pitches_to_tab(pitches: dict, semitone_transpose: int):
    max_simultaneous_notes = max_concurrent_notes(pitches)
    if max_simultaneous_notes > 2:
        raise ValueError(f"got {max_simultaneous_notes} max concurrent notes but humans only have two hands!")

    final_tab = ""
    top_tab = ""
    bottom_tab = ""
    unit_width = get_unit_width() + 2

    ticks_per_line = 12

    for tick_index, tick in enumerate(pitches):
        tick_pitches = pitches.get(tick, None)

        if len(tick_pitches) == 1:
            top_tab += note_to_dulc_tab_string(
                transpose_note(note_from_pitch(tick_pitches[0]), semitone_transpose=semitone_transpose),
                unit_width
            )
            bottom_tab += empty_dulc_tab_string(unit_width)
        elif len(tick_pitches) == 2:
            if tick_pitches[1] > tick_pitches[0]:
                tick_pitches[0], tick_pitches[1] = tick_pitches[1], tick_pitches[0]

            top_tab += note_to_dulc_tab_string(
                transpose_note(note_from_pitch(tick_pitches[0]), semitone_transpose=semitone_transpose),
                unit_width
            )
            bottom_tab += note_to_dulc_tab_string(
                transpose_note(note_from_pitch(tick_pitches[1]), semitone_transpose=semitone_transpose),
                unit_width
            )
        else:
            raise ValueError(f"expect a maximum of 2 pitches per tick, got {len(tick_pitches)}")

        if (tick_index + 1) % ticks_per_line == 0:
            final_tab += f"{top_tab}\n{bottom_tab}\n\n"
            top_tab = ""
            bottom_tab = ""

    final_tab += f"{top_tab}\n{bottom_tab}\n\n"

    return final_tab


options_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Max-Age': '3600',
    'Access-Control-Allow-Credentials': 'true'
}

main_headers = {
    'Access-Control-Allow-Origin': '*'
}


def guitar_to_dulcimer_tab(request: flask.request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        return '', 204, options_headers

    request_json = request.get_json()
    if request_json and 'tab' in request_json:
        tab_string = request_json['tab']
        semitone_transpose = int(request_json['semitoneTranspose'])
    else:
        return 'No guitar tab passed in', 200, main_headers

    dulcimer_tab = guitar_tab_lines_to_dulcimer(
        tab_lines=parse_tab_string(tab_string),
        semitone_transpose=semitone_transpose
    )

    return dulcimer_tab, 200, main_headers


def midi_to_dulcimer_tab(request: flask.request):
    print(f"{request.method}")

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        return '', 204, options_headers

    midi_file = request.files['midi_file']
    midi_save_path = pathlib.Path(f"/tmp/{midi_file.filename}")
    midi_file.save(midi_save_path)

    print(request.form)

    if 'semitoneTranspose' not in request.form:
        return 'No semitoneTranspose passed in', 500, main_headers

    try:
        semitone_transpose = int(request.form['semitoneTranspose'])

        pitches = get_midi_pitches(str(midi_save_path))

        print(f"pitches: {pitches}")

        tab = pitches_to_tab(pitches, semitone_transpose)

        print(f"tab: {tab}")

        return tab, 200, main_headers
    except Exception as e:
        return e, 500, main_headers


#
# def main():
#     with open('bright_side.txt') as tab_file:
#         guitar_tab_string = tab_file.read()
#
#     # guitar_tab_lines = parse_tab_file('tab.txt')
#     guitar_tab_lines = parse_tab_string(guitar_tab_string)
#
#     # print(guitar_tab_lines)
#
#     dulcimer_tab = guitar_tab_lines_to_dulcimer(guitar_tab_lines, semitone_transpose=0)
#     print(dulcimer_tab)
#
#     # for key in list(dulcimer_tab.keys()):
#     #     print(key, dulcimer_tab[key])


def main():
    pitches = get_midi_pitches("Bloaty Dulcimer 1 - transposed.mid")

    print(pitches)
    tab = pitches_to_tab(pitches, 0)
    print(tab)

    # max_notes = max_concurrent_notes(pitches)
    # print(max_notes)


if __name__ == '__main__':
    main()
