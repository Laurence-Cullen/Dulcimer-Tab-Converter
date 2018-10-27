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


def main():
    # tab_lines = read_tab_file('tab.txt')
    # print(tab_lines)

    guitar_string = '|-------------||-----------------5-5----10-9-10-12-10-----7-8-8-10-8-7-------|'

    frets = extract_frets(guitar_string)

    print(frets)


if __name__ == '__main__':
    main()

