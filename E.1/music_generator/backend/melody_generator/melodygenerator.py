from more_itertools import one
import tensorflow.keras as keras
import json
from .preprocess import MAPPING_PATH, SEQUENCE_LENGTH
import numpy as np
import music21 as m21
from midi2audio import FluidSynth


class MelodyGenerator:

    def __init__(self, model_path="C:/Users/laurent/Desktop/music_generator/backend/melody_generator/model/model_final.h5"):

        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH

    def generate_melody(self, seed, num_steps, max_sequence_length, temperature):

        # create seed with symbols
        seed = seed.split()
        melody = seed[:max_sequence_length]
        seed = self._start_symbols + seed[:max_sequence_length]

        # map seed to int
        seed = [self._mappings[symbol]
                for symbol in seed if symbol in self._mappings]
        for _ in range((len(seed) + num_steps)):
            # limit the seed to max seq length
            seed = seed[-max_sequence_length:]

            # encode the seed
            onehot_seed = keras.utils.to_categorical(
                seed, num_classes=len(self._mappings))

            # Transform to 3 dimensions array
            onehot_seed = onehot_seed[np.newaxis, ...]

            # make a prediction
            probabilities = self.model.predict(onehot_seed)[0]

            output_int = self._sample_with_temperature(
                probabilities, temperature)

            # update seed
            seed.append(output_int)

            # map int to our encoding
            output_symbol = [
                k for k, v in self._mappings.items() if v == output_int][0]

            # check whether we're at the end of a melody
            if output_symbol == "/":
                break

            # update the melody
            melody.append(output_symbol)

        return melody

    def _sample_with_temperature(self, probabilities, temperature):
        # temperature -> infinity
        # temperature -> 0
        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p=probabilities)

        return index

    def save_melody(self, melody, step_duration=0.25, format="midi", file_name="mel.mid", speedFactor=1):
        """Converts a melody into a MIDI file
        :param melody (list of str):
        :param min_duration (float): Duration of each time step in quarter length
        :param file_name (str): Name of midi file
        :return:
        """

        # create a music21 stream
        stream = m21.stream.Stream()
        m21.tempo.MetronomeMark(number=180, referent=stream)

        start_symbol = None
        step_counter = 1

        # parse all the symbols in the melody and create note/rest objects
        for i, symbol in enumerate(melody):

            # handle case in which we have a note/rest
            if symbol != "_" or i + 1 == len(melody):

                # ensure we're dealing with note/rest beyond the first one
                if start_symbol is not None:

                    quarter_length_duration = step_duration * step_counter  # 0.25 * 4 = 1

                    # handle rest
                    if start_symbol == "r":
                        m21_event = m21.note.Rest(
                            quarterLength=quarter_length_duration)
                        stream.append(m21_event)

                    # handle note
                    else:
                        if start_symbol.isdigit(): 
                            m21_event = m21.note.Note(
                                int(start_symbol), quarterLength=quarter_length_duration)
                            stream.append(m21_event)

                    # reset the step counter
                    step_counter = 1

                start_symbol = symbol

            # handle case in which we have a prolongation sign "_"
            else:
                step_counter += 1

        # write the m21 stream to a midi file
        stream = stream.scaleOffsets(speedFactor).scaleDurations(speedFactor)
        stream.write(format, file_name)
