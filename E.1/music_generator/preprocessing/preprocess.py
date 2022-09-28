import os
import json
import music21 as m21
import numpy as np
import tensorflow.keras as keras

KERN_DATASET_PATH = "../krn_dataset/erk"
SAVE_DIR = "dataset"
SINGLE_FILE_DATASET = "file_dataset"
MAPPING_PATH = "mapping.json"
SEQUENCE_LENGTH = 64

# durées acceptables
ACCEPTABLE_DURATIONS = [
    0.25, # 16th 
    0.5, # 8th 
    0.75,
    1.0, # quart
    1.5,
    2, # demi note
    3,
    4 # note entière
]


def load_songs_in_kern(dataset_path):
    """Charge les krn et retourne liste de sons (format stream Music21)
    """
    songs = []

    # go through all the files in dataset and load them with music21
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:

            # consider only kern files
            if file[-3:] == "krn":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
    return songs


def has_acceptable_durations(song, acceptable_durations):
    """Retourne True/False en fonction de si le son à une temporalité acceptable ou non:
    """
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_durations:
            return False
    return True


def transpose(song):
    """Transpose le son de sa gamme à  DO majeur OU La mineur
    """

    # Clé du son (Sol ? Fa ?)
    parts = song.getElementsByClass(m21.stream.Part)
    measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = measures_part0[0][4]

    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")

    # Récupere l'intervale (gamme majeure ou mineure)
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # transpose le son dans l'interval donné
    tranposed_song = song.transpose(interval)
    return tranposed_song


def encode_song(song, time_step=0.25):
    """Encode le son en timeSeries:
    """

    encoded_song = []

    for event in song.flat.notesAndRests:

        # Récupere la note
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi # 60
        # récupere le temps de pause
        elif isinstance(event, m21.note.Rest):
            symbol = "r"

        # convertie dans la notation de la timeseries
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):

            # Si la note est la même que la précédente, c'est une prolongation _
            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")

    # relie les notes en string
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song


def preprocess(dataset_path):

    """Lance succéssivement toutes les etapes a la préparation des données:
    """
    print("Loading songs...")
    songs = load_songs_in_kern(dataset_path)
    print(f"Loaded {len(songs)} songs.")

    for i, song in enumerate(songs):

        # Esquive les sons aux temporalités complexes
        if not has_acceptable_durations(song, ACCEPTABLE_DURATIONS):
            continue

        # transpositions des sons
        song = transpose(song)

        # encodage des sons en timeseries
        encoded_song = encode_song(song)

        # sauvegarde des sons en fichier txt
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path, "w") as fp:
            fp.write(encoded_song)

        if i % 10 == 0:
            print(f"Song {i} out of {len(songs)} processed")


def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song


def create_single_file_dataset(dataset_path, file_dataset_path, sequence_length):
    """
    Genere un fichiers contenant tout les sons, avec pour delimiteur / * longueur de sequence
    """

    new_song_delimiter = "/ " * sequence_length
    songs = ""

    # Ajoute les sons et les delimiteurs entre chacuns
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + new_song_delimiter

    # Trim
    songs = songs[:-1]

    # sauvegarde le fichier
    with open(file_dataset_path, "w") as fp:
        fp.write(songs)

    return songs


def create_mapping(songs, mapping_path):
    """Genere un JSON contenant toutes les notes de tout les sons du dataset et leurs quantités
        Afin de donner un "poids" a ces notes
    """
    mappings = {}

    songs = songs.split()
    vocabulary = list(set(songs))

    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i

    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)


def convert_songs_to_int(songs):
    int_songs = []

    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    songs = songs.split()

    for symbol in songs:
        int_songs.append(mappings[symbol])

    return int_songs


def generate_training_sequences(sequence_length):
    """
    Creer l'input et l'output pour l'entrainement du modele
    """

    # charge les sons
    songs = load(SINGLE_FILE_DATASET)
    int_songs = convert_songs_to_int(songs)

    inputs = []
    targets = []

    # genere les training sequences
    num_sequences = len(int_songs) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])

    # encode les sequences
    vocabulary_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)

    print(f"There are {len(inputs)} sequences.")

    return inputs, targets


def main():
    preprocess(KERN_DATASET_PATH)
    songs = create_single_file_dataset(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)
    create_mapping(songs, MAPPING_PATH)


if __name__ == "__main__":
    main()
