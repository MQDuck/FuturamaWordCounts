class StemTable:
    def __init__(self, data=None):
        if data is None:
            self._table = {}
            self._character_sums = {}
            self._stem_sums = {}
        else:
            self._table, self._character_sums, self._stem_sums = data[0], data[1], data[2]

    def use(self, character, stem):
        return self._table[character][stem] if character in self._table and stem in self._table[character] else 0

    def character_use(self, character):
        return self._character_sums[character] if character in self._character_sums else 0

    def stem_use(self, stem):
        return self._stem_sums[stem] if stem in self._stem_sums else 0

    def inc(self, character, stem, val):
        if character in self._table:
            row = self._table[character]
        else:
            row = {}
            self._table[character] = row
        if stem in row:
            row[stem] += val
        else:
            row[stem] = val

        if character in self._character_sums:
            self._character_sums[character] += val
        else:
            self._character_sums[character] = val

        if stem in self._stem_sums:
            self._stem_sums[stem] += val
        else:
            self._stem_sums[stem] = val

    def all_characters(self):
        return self._character_sums.keys()

    def all_stems(self):
        return self._stem_sums.keys()

    def to_tuple(self):
        return self._table, self._character_sums, self._stem_sums
