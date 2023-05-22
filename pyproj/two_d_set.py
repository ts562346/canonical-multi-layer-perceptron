import numpy as np


class two_d_set:
    def __init__(self):
        self.data = []

    def add_array(self, new_arr):
        temp = new_arr[15]
        new_arr[15] = new_arr[14]
        new_arr[14] = temp
        if new_arr not in self.data:
            self.data.append(new_arr)

    def remove_array(self, target_arr):
        self.data.remove(target_arr)

    def get_array(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index):
        return self.data[index]
