from .utils import capacity_of
from .CSRMat import CSRMat

import threading
from typing import Union
from itertools import zip_longest


class Increment(bytearray):

    def __init__(self, byte_array:Union[bytearray,bytes]=b''):
        bytearray.__init__(self, byte_array)

        len_byte_array = len(byte_array)
        self._increment_mat = CSRMat(len_byte_array, len_byte_array + 1, eye=True)
        self._is_changed = False
        self._lock = threading.Lock()

    def reset(self, byte_array:Union[bytearray,bytes]):
        with self._lock:
            bytearray.__setitem__(self, slice(None, None, None), byte_array)

            len_byte_array = len(byte_array)
            self._increment_mat = CSRMat(len_byte_array, len_byte_array + 1, eye=True)
            self._is_changed = False

    def assign(self, byte_array:Union[bytearray,bytes]):
        with self._lock:
            bytearray.__setitem__(self, slice(None, None, None), byte_array)

            len_byte_array = len(byte_array)
            self._increment_mat.indptr = list(range(len_byte_array + 1))
            self._increment_mat.data = [x.to_bytes(1) for x in byte_array]
            self._increment_mat.col_indices = [self._increment_mat._cols - 1] * len_byte_array
            self._increment_mat.row_indices = list(range(len_byte_array))
            self._is_changed = True

    def __insert(self, index:int, value:Union[int,bytearray,bytes]):
        if index < 0 or index > self._increment_mat.rows:
            raise IndexError(index)

        if isinstance(value, int):
            self._increment_mat.insert_row(index)
            self._increment_mat[index, self._increment_mat.cols - 1] = value.to_bytes(1)
        else:
            for i in range(len(value)):
                self._increment_mat.insert_row(index + i)
                self._increment_mat[index + i, self._increment_mat.cols - 1] = value[i].to_bytes(1)

    def insert(self, index:int, value:Union[int,bytearray,bytes]):
        with self._lock:
            if isinstance(value, int):
                bytearray.insert(self, index, value)
            else:
                bytearray.__setitem__(self, slice(index, index), value)

            self.__insert(index, value)
            self._is_changed = True

    def append(self, value:int):
        with self._lock:
            bytearray.append(self, value)

            self._increment_mat.data.append(value.to_bytes(length=1))
            self._increment_mat.col_indices.append(self._increment_mat.cols - 1)
            self._increment_mat.row_indices.append(self._increment_mat.rows)
            self._increment_mat.indptr.append(len(self._increment_mat.data))

            self._is_changed = True

    def extend(self, values:Union[bytes,bytearray]):
        with self._lock:
            bytearray.extend(self, values)

            len_data = len(self._increment_mat.data)
            for value in values:
                self._increment_mat.data.append(value.to_bytes(1))
                len_data += 1

                self._increment_mat.col_indices.append(self._increment_mat.cols - 1)
                self._increment_mat.row_indices.append(self._increment_mat.rows)
                self._increment_mat.indptr.append(len_data)
            self._is_changed = True

    def __process_slice(self, index:Union[int,slice]):
        len_self = len(self)

        if isinstance(index, int):
            if index < 0:
                index += len_self

            return index, index+1, 1

        start = index.start
        stop = index.stop
        step = index.step
        if step is None:
            step = 1

        if start is None:
            start = (0 if step > 0 else len_self - 1)
        elif start < 0:
            start += len_self
        
        if stop is None:
            stop = (len_self if step > 0 else -1)
        elif stop < 0:
            stop += len_self

        if stop > len_self:
            stop = len_self

        if start > len_self:
            start = len_self

        return start, stop, step

    def __set_one_item(self, index:int, value:int):
        if index < 0 or index >= self._increment_mat.rows:
            raise IndexError(index)

        start = self._increment_mat.indptr[index]
        stop = self._increment_mat.indptr[index + 1]
        if stop - start == 1:
            self._increment_mat.data[start] = value.to_bytes(1)
            self._increment_mat.col_indices[start] = self._increment_mat.cols - 1
        else:
            self._increment_mat.reset_row(index)
            self._increment_mat[index, self._increment_mat.cols - 1] = value.to_bytes(1)

    def __setitem__(self, index:Union[int,slice], value:Union[int,bytes,bytearray]):
        with self._lock:
            start, stop, step = self.__process_slice(index)
            bytearray.__setitem__(self, index, value)

            if isinstance(index, int):
                self.__set_one_item(index, value)
            else:
                indices = list(range(start, stop, step))
                len_indices = len(indices)
                len_value = len(value)
                last_index = start-1
                for i, sub_value in zip_longest(indices, value):
                    if i is None or sub_value is None:
                        break
                    
                    self.__set_one_item(i, sub_value)
                    last_index = i

                if len_indices < len_value:
                    self.__insert(last_index+1, value[len_indices:])
                elif len_indices > len_value:
                    self.__delitem(last_index+1, last_index+1+len_indices-len_value)

            self._is_changed = True

    def __delitem(self, start:int, stop:int=None, step:int=1):
        if stop is None:
            stop = start + 1

        if step != 1:
            delta = 0
            for i in range(start, stop, step):
                self._increment_mat.remove_row(i-delta)
                delta += 1
        else:
            self._increment_mat.remove_row(start, stop)

    def __delitem__(self, index:Union[int,slice]):
        with self._lock:
            start, stop, step = self.__process_slice(index)
            bytearray.__delitem__(self, index)
            self.__delitem(start, stop, step)
            self._is_changed = True

    def __str__(self):
        return bytearray.__str__(self)
    
    def __repr__(self):
        return bytearray.__repr__(self)

    def pop(self, index:int=-1):
        with self._lock:
            index, _, _ = self.__process_slice(index)
            result = bytearray.pop(self, index)
            self.__delitem(index)
            self._is_changed = True

            return result

    def remove(self, value:int):
        with self._lock:
            index = bytearray.index(self, value)
            bytearray.remove(self, value)
            self.__delitem(index)
            self._is_changed = True

    def clear(self):
        with self._lock:
            if len(self) == 0:
                return
        
            bytearray.clear(self)

            if self._increment_mat.rows > 0:
                self._increment_mat.indptr = [0]
                self._increment_mat.col_indices = []
                self._increment_mat.row_indices = []
                self._increment_mat.data = []
                self._is_changed = True

    def patch(self):
        with self._lock:
            self_cols = self._increment_mat.cols
            self_rows = self._increment_mat.rows

            result = {
                "move": [],
                "update": [],
                "new_data": bytearray(),
                "old_size": self_cols - 1,
                "new_size": self_rows,
                "old_capacity": capacity_of(self_cols - 1),
                "new_capacity": capacity_of(self_rows),
            }

            if not self._is_changed:
                return result

            col_dict = {}
            for i, j, d in zip(
                self._increment_mat.row_indices,
                self._increment_mat.col_indices,
                self._increment_mat.data
            ):
                if j not in col_dict:
                    col_dict[j] = {}
                col_dict[j][i] = d

            self_cols_1 = self_cols - 1

            if self_cols_1 in col_dict:
                last_i = -2
                update = None
                len_new_data = len(result["new_data"])
                for i, d in col_dict[self_cols_1].items():
                    result["new_data"].extend(d)
                    len_new_data += 1
                    if i != last_i + 1:
                        update = {"dest_start": i, "src_start": len_new_data - 1, "size": 1}
                        result["update"].append(update)
                    else:
                        update["size"] += 1

                    last_i = i

            delta = 0
            move = None
            for j in sorted(col_dict.keys()):
                if len(col_dict[j]) != 1 or j == self_cols_1:
                    continue

                for i in col_dict[j]:
                    assert col_dict[j][i] == 1
                    current_delta = i - j
                    if current_delta == 0:
                        continue

                    if current_delta != delta:
                        move = {"old_start": j, "size": 1, "new_start": i, "is_moved": False, "current_start": j}
                        result["move"].append(move)
                        delta = current_delta
                    else:
                        move["size"] += 1

            self._increment_mat = CSRMat(self_rows, self_rows + 1, eye=True)
            self._is_changed = False

            return result

    @property
    def is_changed(self):
        return self._is_changed

    def __apply_move(self, move):
        new_start = move["new_start"]
        old_start = move["old_start"]
        nbytes = move["size"]
        self[new_start:new_start+nbytes] = self[old_start:old_start+nbytes]
        move["is_moved"] = True
        move["current_start"] = new_start

    def apply_patch(self, patch):
        if patch["old_size"] < patch["new_size"]:
            self.extend(bytes(patch["new_size"] - patch["old_size"]))

        len_move = len(patch["move"])
        has_moved = True
        while has_moved:
            has_moved = False
            for i, move in enumerate(patch["move"]):
                if move["is_moved"]:
                    continue

                new_start = move["new_start"]
                old_start = move["old_start"]
                nbytes = move["size"]
                if new_start > old_start:
                    if i + 1 < len_move:
                        if new_start + nbytes <= patch["move"][i + 1]["current_start"]:
                            self.__apply_move(move)
                            has_moved = True
                    else:
                        self.__apply_move(move)
                        has_moved = True
                else:
                    if i - 1 >= 0:
                        if new_start >= patch["move"][i - 1]["current_start"] + patch["move"][i - 1]["size"]:
                            self.__apply_move(move)
                            has_moved = True
                    else:
                        self.__apply_move(move)
                        has_moved = True

        if patch["old_size"] > patch["new_size"]:
            del self[patch["new_size"]:]

        new_data = patch["new_data"]
        patch_update = patch["update"]

        if new_data and patch_update:
            if len(patch_update) > 1:
                for update in patch_update:
                    dest_start = update["dest_start"]
                    size = update["size"]
                    src_start = update["src_start"]
                    self[dest_start:dest_start+size] = new_data[src_start:src_start+size]
            else:
                update = patch_update[0]
                dest_start = update["dest_start"]
                size = update["size"]
                self[dest_start:dest_start+size] = new_data
