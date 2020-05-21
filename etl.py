import tensorflow as tf
from machine import ConfiguredMachine
from faker import Faker
import re
import pickle

class EnigmaDataProcessor:
    def __init__(self, max_len=42, char_tokenizer=None):
        self.max_len = max_len
        self.char_tokenizer = char_tokenizer
        self._fake = Faker()
        self._machine = ConfiguredMachine()

    def _strip_and_captitalize(self, text):
        """Clean text by keeping only alphabetical characters and captitalizing them

        Args:
            text (str): text to be processed

        Returns:
            str: string with only capitalized alphabectical characters
        """
        return re.sub('[^a-zA-Z]', '', text).upper()

    def _add_start_end_tokens(self, text_list):
        """Add start and end tokens to strings in text list
        
        Args:
            text_list (str): list of strings
            
        Returns:
            list: list of formatted strings
        """
        return [f"s{s}e" for s in text_list]

    def generate_text(self, size):
        """Generate enigma machine data

        Args:
            size (int): number of sequences to generate

        Returns:
            list, list: tuple of two lists. First is the encoded text, second is the decoded text
        """
        plain_list = self._fake.texts(nb_texts=size, max_nb_chars=self.max_len)
        plain_list = [self._strip_and_captitalize(p) for p in plain_list]
        cipher_list = self._machine.batch_encode(plain_list)
        plain_list = self._add_start_end_tokens(plain_list)
        cipher_list = self._add_start_end_tokens(cipher_list)
        return cipher_list, plain_list

    def _vectorize_and_pad(self, text_list):
        """Convert text to list of numbers and pad sequences at the end until they are of size self.max_len + 2
        Adding 2 accounts for the start and end tokens

        Args:
            text_list (str): list of string

        Returns:
            np.array: numpy array of size len(text_list) x self.max_len + 2
        """
        arr = self.char_tokenizer.texts_to_sequences(text_list)
        arr = tf.keras.preprocessing.sequence.pad_sequences(arr, maxlen=self.max_len + 2, padding='post')
        return arr

    def text_to_numbers(self, cipher_list, plain_list):
        """Convert enigma encoded and decoded sequences to numerical arrays

        Args:
            cipher_list (list): list of encoded texts as strings
            plain_list (list): list of decoded texts as strings

        Returns:
            np.array, np.array: Numerical representations of the encoded and decoded text, respectively
        """
        
        if not self.char_tokenizer:
            self.char_tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True, lower=False)
            self.char_tokenizer.fit_on_texts(plain_list)

        cipher_array = self._vectorize_and_pad(cipher_list)
        plain_array = self._vectorize_and_pad(plain_list)
        return cipher_array, plain_array

    def generate_examples(self, size):
        """Generate examples for model

        Args:
            size (int): number of sequences to generate

        Returns:
            td.data.Dataset: Numerical representations of the encoded and decoded text as tensors
        """
        cipher_list, plain_list = self.generate_text(size)
        cipher_array, plain_array = self.text_to_numbers(cipher_list, plain_list)
        dataset = tf.data.Dataset.from_tensor_slices((cipher_array, plain_array))
        return dataset

    def save_tokenizer(self, path):
        with open(path, "wb") as handle:
            pickle.dump(self.char_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

