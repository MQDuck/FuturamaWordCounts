class WordTable:
    def __init__(self, data=None):
        if data is None:
            self._table = {}
            self._character_sums = {}
            self._word_sums = {}
        else:
            self._table, self._character_sums, self._word_sums = data[0], data[1], data[2]

    def use(self, character, word):
        return self._table[character][word] if character in self._table and word in self._table[character] else 0

    def character_use(self, character):
        return self._character_sums[character] if character in self._character_sums else 0

    def word_use(self, word):
        return self._word_sums[word] if word in self._word_sums else 0

    def inc(self, character, word, val):
        if character in self._table:
            row = self._table[character]
        else:
            row = {}
            self._table[character] = row
        if word in row:
            row[word] += val
        else:
            row[word] = val

        if character in self._character_sums:
            self._character_sums[character] += val
        else:
            self._character_sums[character] = val

        if word in self._word_sums:
            self._word_sums[word] += val
        else:
            self._word_sums[word] = val

    def all_charcters(self):
        return self._character_sums.keys()

    def all_words(self):
        return self._word_sums.keys()

    def to_tuple(self):
        return self._table, self._character_sums, self._word_sums
