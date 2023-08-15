from .utils import capacity_of
from .CSRMat import CSRMat

import threading

class Increment(CSRMat):
    def __init__(self, _list):
        len_list = len(_list)
        CSRMat.__init__(self, len_list, len_list+1, eye=True)
        self._is_changed = False
        self._lock = threading.Lock()

    def reset(self, _list):
        len_list = len(_list)
        self.indptr = list(range(len_list+1))
        self.data = _list
        self.col_indices = [self._cols-1] * len_list
        self.row_indices = list(range(len_list))

    def insert(self, index, value):
        with self._lock:
            if index < 0 or index > self.rows:
                raise IndexError(index)

            if isinstance(value, list):
                for i in range(len(value)):
                    self.insert_row(index+i)
                    self[index+i, self.cols-1] = value[i]
            else:
                self.insert_row(index)
                self[index, self.cols-1] = value

            self._is_changed = True

    def append(self, value):
        with self._lock:
            len_data = len(self.data)
            if isinstance(value, list):
                for sub_value in value:
                    self.data.append(sub_value)
                    len_data += 1

                    self.col_indices.append(self.cols-1)
                    self.row_indices.append(self.rows)
                    self.indptr.append(len_data)
            else:
                self.data.append(value)
                self.col_indices.append(self.cols-1)
                self.row_indices.append(self.rows)
                self.indptr.append(len_data)

            self._is_changed = True

    def update(self, index, value):
        if isinstance(index, list):
            len_index = len(index)
            if not isinstance(value, list):
                value = [value]*len_index
            for i in range(len_index):
                self.update(index[i], value[i])
            return

        with self._lock:
            if index < 0 or index >= self.rows:
                raise IndexError(index)

            start = self.indptr[index]
            stop = self.indptr[index+1]
            if stop - start == 1:
                self.data[start] = value
                self.col_indices[start] = self.cols-1
            else:
                self.reset_row(index)
                self[index, self.cols-1] = value

            self._is_changed = True

    def delete(self, start, stop=None):
        with self._lock:
            self.remove_row(start, stop)
            self._is_changed = True

    def clear(self):
        with self._lock:
            if self.rows > 0:
                self.indptr = [0]
                self.col_indices = []
                self.row_indices = []
                self.data = []
                self._is_changed = True

    def patch(self):
        with self._lock:
            self_cols = self.cols
            self_rows = self.rows
            
            result = \
            {
                "move": [],
                "update": [],
                "new_data": [],
                "old_size": self_cols-1,
                "new_size": self_rows,
                "old_capacity": capacity_of(self_cols-1),
                "new_capacity": capacity_of(self_rows)
            }

            if not self._is_changed:
                return result
            
            col_dict = {}
            for i, j, d in zip(self.row_indices, self.col_indices, self.data):                
                if j not in col_dict:
                    col_dict[j] = {}
                col_dict[j][i] = d

            self_cols_1 = self_cols-1

            last_i = -2
            update = None
            len_new_data = len(result["new_data"])
            for i, d in col_dict[self_cols_1].items():
                result["new_data"].append(d)
                len_new_data += 1
                if i != last_i+1:
                    update = \
                    {
                        "dest_start": i,
                        "src_start": len_new_data - 1,
                        "size": 1
                    }
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
                        move = \
                        {
                            "old_start": j,
                            "size": 1,
                            "new_start": i
                        }
                        result["move"].insert(0, move)
                        delta = current_delta
                    else:
                        move["size"] += 1

            CSRMat.__init__(self, self_rows, self_rows+1, eye=True)
            self._is_changed = False

            return result

    @property
    def is_changed(self):
        return self._is_changed