from .utils import di

class ExtendableList:

    class iterator:
        def __init__(self, _list):
            self.__list = _list
            self.__len_list = len(_list)
            self.__current_index = 0

        def __next__(self):
            if self.__current_index >= self.__len_list:
                raise StopIteration()
            
            value = self.__list[self.__current_index]
            self.__current_index += 1

            return value
        
        def __iter__(self):
            self.__current_index = 0
            return self

    def __init__(self, strong_ref:bool=True):
        self._strong_ref = strong_ref
        self._list = []

    def __setitem__(self, index, value):
        len_self = len(self)
        if isinstance(index, int) and index >= len_self:
            self._list.extend([id(None)]*(index-len_self+1))
        
        if self._strong_ref:
            self._list[index] = value
        else:
            self._list[index] = id(value)

    def __getitem__(self, index):
        value = self._list[index]
        if self._strong_ref:
            return value
        else:
            if isinstance(index, slice):
                return list(map(lambda x:di(x), value))
            else:
                return di(value)
            
    def __delitem__(self, index):
        del self._list[index]
        
    def __contains__(self, value):
        if self._strong_ref:
            return value in self._list
        else:
            return id(value) in self._list
        
    def __len__(self):
        return self._list.__len__()
    
    def __bool__(self):
        return bool(self._list)
    
    def __iter__(self):
        return ExtendableList.iterator(self)
    
    def append(self, value):
        if self._strong_ref:
            self._list.append(value)
        else:
            self._list.append(id(value))

    def insert(self, index, value):
        if self._strong_ref:
            self._list.insert(index, value)
        else:
            self._list.insert(index, id(value))

    def extend(self, value_list):
        if self._strong_ref:
            self._list.extend(value_list)
        else:
            self._list.extend(map(lambda x:id(x), value_list))

    def remove(self, value):
        if self._strong_ref:
            self._list.remove(value)
        else:
            self._list.remove(id(value))

    def pop(self, index):
        value = self._list.pop(index)
        if self._strong_ref:
            return value
        else:
            return id(value)
        
    def clear(self):
        self._list.clear()

class DictList(ExtendableList):
    def __init__(self, values:(list,dict)=None, strong_ref:bool=True, **kwargs):
        ExtendableList.__init__(self, strong_ref)

        self._key_index_map = {}
        self._key_list = ExtendableList()

        if isinstance(values, list):
            self.extend(values)
        elif isinstance(values, dict):
            self.update(values)

        self.update(kwargs)
    
    def __setitem__(self, index:(int,slice,str), value):
        if isinstance(index, str):
            key = index
            if key in self._key_index_map:
                index = self._key_index_map[key]
                ExtendableList.__setitem__(self, index, value)
            else:
                len_self = len(self)
                self._key_index_map[key] = len_self
                self._key_list[len_self] = key
                ExtendableList.append(self, value)
        else:
            ExtendableList.__setitem__(self, index, value)

    def __getitem__(self, index:(int,slice,str)):
        if isinstance(index, str):
            key = index
            index = self._key_index_map[key]

        return ExtendableList.__getitem__(self, index)
    
    def __update_after(self, index):
        for i in range(index, len(self._key_list)):
            key = self._key_list[i]
            if key is not None:
                self._key_index_map[key] = i

    def __delitem__(self, index:(int,str,slice)):
        if isinstance(index, slice):
            start, stop, step = self._process_slice(index)
            for i in range(start, stop, step):
                del self[i]
            return

        key = None
        if isinstance(index, str):
            key = index
            index = self._key_index_map[key]
        elif isinstance(index, int):
            key = self._key_list[index]

        if key is not None:
            del self._key_index_map[key]

        del self._key_list[index]
        ExtendableList.__delitem__(self, index)
        
        self.__update_after(index)

    def pop(self, index:(int,str)):
        key = None
        if isinstance(index, str):
            key = index
            index = self._key_index_map[key]
        elif isinstance(index, int):
            key = self._key_list[index]

        if key is not None:
            del self._key_index_map[key]

        del self._key_list[index]
        value = ExtendableList.pop(self, index)
        
        self.__update_after(index)

        return value
        
    def insert(self, index:(int,str), value, key:str=None):
        if isinstance(index, str):
            index = self._key_index_map[index]

        ExtendableList.insert(self, index, value)
        self._key_list.insert(index, key)
        if key is not None:
            self._key_index_map[key] = index

        self.__update_after(index+1)

    def append(self, value, key:str=None):
        ExtendableList.append(self, value)
        self._key_list.append(key)
        if key is not None:
            self._key_index_map[key] = len(self)-1

    def extend(self, new_list):
        ExtendableList.extend(self, new_list)
        self._key_list.extend([None]*len(new_list))
    
    def update(self, new_dict):
        for key, value in new_dict.items():
            self[key] = value

    def index(self, key:str)->int:
        return self._key_index_map[key]

    def key(self, index:int)->str:
        return self._key_list[index]
        
    def clear(self):
        ExtendableList.clear(self)
        self._key_index_map.clear()
        self._key_list.clear()
        
    def __contains__(self, key)->bool:
        if isinstance(key, str):
            return (key in self._key_index_map)
        else:
            return ExtendableList.__contains__(self, key)

    def keys(self):
        return self._key_index_map.keys()