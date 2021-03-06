bottom_string = 'E'

octave0 = ["Eb"]
octave1 = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
octave2 = ["e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#"]
octave3 = ["e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "b'", "c'", "c#'", "d'", "d#'"]
octave4 = ["e''", "f''", "f#''", "g''", "g#''", "a''", "a#''", "b''", "c''", "c#''", "d''", "d#''"]

all_notes = octave0 + octave1 + octave2 + octave3 + octave4

midi_pitch_to_note = {
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
