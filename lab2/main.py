from typing import Self

class LongNatural:
    def __init__(self, digits: str):
        self.digits = digits.lstrip('0') or '0'
    
    def __add__(self, other: Self):
        carry = 0
        res = ""
        for i in range(0, max(len(self.digits), len(other.digits))):
            a = int(self.digits[-i-1]) if i < len(self.digits) else 0
            b = int(other.digits[-i-1]) if i < len(other.digits) else 0
            sum = a + b + carry
            carry = sum // 10
            res = str(sum % 10) + res
        if carry != 0: 
            res = str(carry) + res
        return LongNatural(res)
    
    def __sub__(self, other):
        # исходим из того что self больше
        borrow = 0
        res = ""
        for i in range(len(self.digits)):
            a = int(self.digits[-i-1])
            b = int(other.digits[-i-1]) if i < len(other.digits) else 0
            diff = a - b - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            res = str(diff) + res
        res = res.lstrip('0') or '0'
        return LongNatural(res.lstrip('0') or '0')
    
    def is_zero(self):
        return self.digits == "" or self.digits == "0"

    def __str__(self):
        return self.digits

    def __mul__(self, other: Self) -> Self:
        if self.is_zero() or other.is_zero():
            return LongNatural("0")
        
        if len(self.digits) == 1:
            d = int(self.digits)
            carry = 0
            res = ""
            for digit in other.digits[::-1]:
                prod = int(digit) * d + carry
                carry = prod // 10
                res = str(prod % 10) + res
            if carry:
                res = str(carry) + res
            return LongNatural(res)
        elif len(other.digits) == 1:
            return other * self
        
        n = min(len(self.digits), len(other.digits)) // 2
        if n == 0: 
            n = 1
        a = LongNatural(self.digits[-n:])
        b = LongNatural(self.digits[:-n] or "0")
        c = LongNatural(other.digits[-n:])
        d = LongNatural(other.digits[:-n] or "0")
        
        p1 = a * c
        p2 = b * d
        p3 = (a + b) * (c + d) - p1 - p2
        p2_shifted = LongNatural(p2.digits + "0" * (2 * n))
        p3_shifted = LongNatural(p3.digits + "0" * n)
        
        return p1 + p2_shifted + p3_shifted

    def __eq__(self, value: Self) -> bool:
        return (self.is_zero() and value.is_zero()) or (self.digits == value.digits)
    
    def __ne__(self, value: Self) -> bool:
        return not(self == value)
    
    def __lt__(self, other: Self) -> bool:
        if len(self.digits) < len(other.digits):
            return True 
        else:
            for i in range(len(self.digits)):
                a = int(self.digits[i])
                b = int(other.digits[i - len(self.digits) + len(other.digits)]) if i - len(self.digits) + len(other.digits) >= 0 else 0
                if a == b:
                    continue
                else:
                    return a < b
            return False
    
    def __le__(self, other: Self) -> bool:
        return self == other or self < other
    
    def __gt__(self, other):
        return other < self
    
    def __ge__(self, other):
        return other <= self

class LongInteger:
    def __init__(self, s: str):
        self.sign = "-" if s[0] == "-" else ""
        self.abs = LongNatural(s.replace("-", ""))
    
    def __str__(self):
        return self.sign + self.abs.digits
    
    def __add__(self, other: Self) -> Self:
        if self.sign == other.sign:
            res_abs = self.abs + other.abs
            return LongInteger(self.sign + res_abs.digits)
        else:
            if self.abs > other.abs:
                res_abs = self.abs - other.abs
                return LongInteger(self.sign + res_abs.digits)
            elif other.abs > self.abs:
                res_abs = other.abs - self.abs
                return LongInteger(other.sign + res_abs.digits)
            else:
                return LongInteger("0")
    
    def __sub__(self, other: Self) -> Self:
        return self + LongInteger({"": "-", "-": ""}[other.sign] + other.abs.digits)
    
    def is_zero(self) -> bool:
        return self.abs.is_zero()
    
    def __eq__(self, value: Self) -> bool:
        return (self.is_zero() and value.is_zero()) or (self.abs == value.abs and self.sign == value.sign)
    
    def __ne__(self, value):
        return not(self == value)
    
    def __lt__(self, other: Self) -> bool:
        return (self - other).sign == "-"
    
    def __le__(self, other: Self) -> bool:
        return self < other or self == other
    
    def __ge__(self, other: Self) -> bool:
        return other < self 
    
    def __gt__(self, other: Self) -> bool:
        return other <= self

def run_tests():
    print("--- Запуск тестов ---")
    
    # Тесты LongNatural
    print("\n[LongNatural Tests]")
    
    # Сложение
    assert str(LongNatural("123") + LongNatural("456")) == "579", "Fail: 123+456"
    assert str(LongNatural("999") + LongNatural("1")) == "1000", "Fail: 999+1 carry"
    assert str(LongNatural("0") + LongNatural("0")) == "0", "Fail: 0+0"
    print("OK: Addition")
    
    # Вычитание
    assert str(LongNatural("500") - LongNatural("200")) == "300", "Fail: 500-200"
    assert str(LongNatural("1000") - LongNatural("1")) == "999", "Fail: 1000-1 borrow"
    print("OK: Subtraction")
    
    # Умножение
    assert str(LongNatural("12") * LongNatural("12")) == "144", "Fail: 12*12"
    assert str(LongNatural("123456") * LongNatural("789")) == "97406784", "Fail: Karatsuba large"
    assert str(LongNatural("0") * LongNatural("100")) == "0", "Fail: Zero mult"
    print("OK: Multiplication")
    
    # Сравнение
    assert (LongNatural("100") > LongNatural("99")), "Fail: length compare"
    assert (LongNatural("123") < LongNatural("124")), "Fail: digit compare"
    assert (LongNatural("007") == LongNatural("7")), "Fail: leading zeros eq"
    print("OK: Comparisons")

    # Тесты LongInteger
    print("\n[LongInteger Tests]")
    
    # Сложение знаков
    assert str(LongInteger("-5") + LongInteger("-3")) == "-8", "Fail: neg+neg"
    assert str(LongInteger("10") + LongInteger("-3")) == "7", "Fail: pos+neg (result pos)"
    assert str(LongInteger("3") + LongInteger("-10")) == "-7", "Fail: pos+neg (result neg)"
    assert str(LongInteger("-5") + LongInteger("5")) == "0", "Fail: cancel to zero"
    print("OK: Signed Addition")
    
    # Вычитание
    assert str(LongInteger("10") - LongInteger("20")) == "-10", "Fail: pos - pos = neg"
    assert str(LongInteger("-5") - LongInteger("-2")) == "-3", "Fail: neg - neg"
    print("OK: Signed Subtraction")
    
    # Сравнение
    assert (LongInteger("-10") < LongInteger("5")), "Fail: neg < pos"
    assert (LongInteger("-20") < LongInteger("-10")), "Fail: neg < neg"
    print("OK: Signed Comparisons")

    print("\n--- Все тесты пройдены успешно ---")

if __name__ == "__main__":
    print(f"Visual Check 1: {LongNatural('8009') + LongNatural('9912')} == 17921")
    print(f"Visual Check 2: {LongNatural('155555') * LongNatural('300')} == 46666500")
    print(f"Visual Check 3: {LongNatural('9000') <= LongNatural('9000')} == True")
    
    run_tests()