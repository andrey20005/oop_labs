from numbers import Number


class Vector:
    def __init__(self, *elems: Number, size:int=0, d:Number=0):
        self.elems = list(elems)
        if size:
            while len(self.elems) < size:
                self.elems.append(d)
    
    def get(self, i: int) -> Number:
        return self.elems[i]
    
    def set(self, i: int, el: Number):
        self.elems[i] = el
    
    def __len__(self):
        return len(self.elems)
    
    def __str__(self):
        return str(self.elems)

class CheckedVector(Vector):
    def get(self, i: int) -> Number:
        if i < 0 and len(self) <= i: 
            raise IndexError(f"Индекс неправильный {i}. len(self)={len(self)}")
        return super().get(i)
    
    def set(self, i: int, el: Number):
        if i < 0 or len(self) <= i: 
            raise IndexError(f"Индекс неправильный {i}. len(self)={len(self)}")
        super().set(i, el)

class SortedVector(Vector):
    def __init__(self, *elems, size = 0, d = 0):
        super().__init__(*elems, size=size, d=d)
        self.elems = sorted(self.elems)
    
    def set(self, i, el):
        super().set(i, el)
        self.elems = sorted(self.elems)

class SortedCheckedVector(SortedVector, CheckedVector):
    pass

if __name__ == "__main__":
    a = SortedCheckedVector(6, 3, 9, 2, 9)
    print(a)
    a.set(2, 15)
    print(a)
    a.set(15, 6)

