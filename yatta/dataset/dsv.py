"""
Dataset reader that reads data from a CSV/TSV file.
"""

import csv
from tqdm import tqdm


class DSVDataset():
    """
    Dataset reader that reads data from a CSV/TSV file. Takes filename as
    input. All other kwargs are passed onto csv.DictReader.
    """
    def __init__(self, file_path, delimiter=",", verbose=False, **kwargs):
        self.verbose = verbose
        self.file_path = file_path
        self.delimiter = delimiter
        self.data = list(self.read(**kwargs))
        if self.verbose:
            print("Read {} rows from {}".format(len(self.data), self.file_path))

    def read(self, **kwargs):
        if self.verbose:
            print("Reading data from {}".format(self.file_path))
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=self.delimiter, **kwargs)
            for row in tqdm(reader, disable=not self.verbose):
                yield row

    def __getitem__(self, idx: str):
        return self.data[int(idx)]

    def __len__(self):
        return len(self.data)
