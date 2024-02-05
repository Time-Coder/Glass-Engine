class CSRMat:

    def __init__(self, rows: int, cols: int = None, eye: bool = False) -> None:
        if cols is None:
            cols = rows

        self._cols = cols
        if eye:
            n = min(rows, cols)

            self.indptr = list(range(n + 1))
            if rows > n:
                self.indptr.extend((rows + 1 - n) * [n])

            self.col_indices = list(range(n))
            self.row_indices = list(range(n))
            self.data = n * [1]
        else:
            self.indptr = (rows + 1) * [0]
            self.col_indices = []
            self.row_indices = []
            self.data = []

    def __getitem__(self, ij) -> object:
        i, j = ij

        start_index = self.indptr[i]
        end_index = self.indptr[i + 1]
        cols = self.col_indices[start_index:end_index]
        try:
            index_j = cols.index(j)
            return self.data[start_index + index_j]
        except:
            return 0

    def __setitem__(self, ij: tuple, value: object) -> None:
        if value == 0:
            self.__delitem__(ij)
            return

        i, j = ij

        start_index = self.indptr[i]
        end_index = self.indptr[i + 1]
        cols = self.col_indices[start_index:end_index]
        try:
            index_j = cols.index(j)
            self.data[start_index + index_j] = value
        except:
            self.col_indices.insert(self.indptr[i], j)
            self.row_indices.insert(self.indptr[i], i)
            self.data.insert(self.indptr[i], value)
            for k in range(i + 1, len(self.indptr)):
                self.indptr[k] += 1

    def __delitem__(self, ij: tuple) -> None:
        i, j = ij

        if i < 0 or i >= self.rows:
            raise IndexError(j)

        if j < 0 or j >= self.cols:
            raise IndexError(j)

        start_index = self.indptr[i]
        end_index = self.indptr[i + 1]
        cols = self.col_indices[start_index:end_index]
        try:
            index_j = cols.index(j)
            del self.data[start_index + index_j]
            del self.col_indices[start_index + index_j]
            del self.row_indices[start_index + index_j]
            for k in range(i + 1, len(self.indptr)):
                self.indptr[k] -= 1
        except:
            pass

    @property
    def rows(self) -> int:
        return self.indptr.__len__() - 1

    @property
    def cols(self) -> int:
        return self._cols

    def __repr__(self) -> str:
        result = ""
        rows = self.rows
        cols = self.cols
        for i in range(rows):
            for j in range(cols):
                result += str(self[i, j])
                if j < cols - 1:
                    result += " "
            if i < rows - 1:
                result += "\n"
        return result

    def insert_row(self, i: int, n: int = 1) -> None:
        for _ in range(n):
            self.indptr.insert(i, self.indptr[i])

    def append_row(self, n: int = 1) -> None:
        for _ in range(n):
            self.indptr.insert(self.rows, self.indptr[self.rows])

    def reset_row(self, row_start: int, row_end: int = None) -> None:
        if row_end is None:
            row_end = row_start + 1

        if row_end == row_start:
            return

        start = self.indptr[row_start]
        stop = self.indptr[row_end]
        del self.col_indices[start:stop]
        del self.row_indices[start:stop]
        del self.data[start:stop]
        delta = stop - start
        for it in range(row_end, len(self.indptr)):
            self.indptr[it] -= delta

    def remove_row(self, row_start: int, row_end: int = None) -> None:
        if row_end is None:
            row_end = row_start + 1

        if row_end == row_start:
            return

        del self.col_indices[self.indptr[row_start] : self.indptr[row_end]]
        del self.row_indices[self.indptr[row_start] : self.indptr[row_end]]
        del self.data[self.indptr[row_start] : self.indptr[row_end]]
        del self.indprt[row_start:row_end]
