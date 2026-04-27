from typing import Self

class LongNatural:
    def __init__(self, digits: str):
        self.digits = digits.lstrip('0') or '0'

    def __str__(self) -> str:
        return self.digits
    
    def is_zero(self) -> bool:
        return self.digits == "" or self.digits == "0"
    
    def __add__(self, other: Self) -> Self:
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
    
    def __sub__(self, other: Self) -> Self:
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
        return LongNatural(res.lstrip('0') or '0')

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
    
    def __floordiv__(self, other: Self) -> Self:
        low, high = LongNatural("1"), self
        mids = []
        while len(mids) <= 2 or mids[-2] != mids[-1]:
            mid = LongNatural(((low + high + LongNatural("0")) * LongNatural("5")).digits[:-1])
            mids.append(mid)
            prod = mid * other
            if prod <= self:
                low = mid 
            else:
                high = mid 
        return mids[-1] 
    
    def __mod__(self, other: Self) -> Self:
        return self - self // other * other


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
    
    def __mul__(self, other: Self) -> Self:
        return LongInteger(("-" if (self.sign == "-") != (other.sign == "-") else "") + (self.abs * other.abs).digits)
    
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
    
    def __floordiv__(self, other: Self) -> Self:
        q_abs = self.abs // other.abs
        r_abs = self.abs % other.abs
        
        signs_differ = (self.sign == "-") ^ (other.sign == "-")
        
        if signs_differ:
            if r_abs.is_zero():
                result_digits = q_abs.digits if not q_abs.is_zero() else "0"
                return LongInteger("-" + result_digits if result_digits != "0" else "0")
            else:
                q_abs = q_abs + LongNatural("1")
                result_digits = q_abs.digits if not q_abs.is_zero() else "0"
                return LongInteger("-" + result_digits if result_digits != "0" else "0")
        else:
            return LongInteger(q_abs.digits)
    
    def __mod__(self, other: Self) -> Self:
        return self - (self // other) * other

if __name__ == "__main__":
    print(f"{LongNatural('123') + LongNatural('456')} | {123 + 456}")
    print(f"{LongNatural('999') + LongNatural('1')} | {999 + 1}")
    print(f"{LongNatural('0') + LongNatural('42')} | {0 + 42}")
    print(f"{LongNatural('456') - LongNatural('123')} | {456 - 123}")
    print(f"{LongNatural('1000') - LongNatural('1')} | {1000 - 1}")

    print(f"{LongNatural('12') * LongNatural('34')} | {12 * 34}")
    print(f"{LongNatural('0') * LongNatural('123')} | {0 * 123}")
    print(f"{LongNatural('123456789') * LongNatural('987654321')} | {123456789 * 987654321}")
    
    print(f"{LongNatural('10') // LongNatural('3')} | {10 // 3}")
    print(f"{LongNatural('10') % LongNatural('3')} | {10 % 3}")
    
    print(f"{LongNatural('123') < LongNatural('456')} | {123 < 456}")
    print(f"{LongNatural('123') == LongNatural('123')} | {123 == 123}")
    

    print(f"{LongInteger('10') + LongInteger('-3')} | {10 + (-3)}")
    print(f"{LongInteger('-10') + LongInteger('3')} | {-10 + 3}")
    print(f"{LongInteger('-10') + LongInteger('-20')} | {-10 + (-20)}")
    print(f"{LongInteger('10') - LongInteger('3')} | {10 - 3}")
    
    print(f"{LongInteger('12') * LongInteger('3')} | {12 * 3}")
    print(f"{LongInteger('-12') * LongInteger('3')} | {-12 * 3}")
    print(f"{LongInteger('-12') * LongInteger('-3')} | {-12 * (-3)}")
    
    print(f"{LongInteger('10') // LongInteger('3')} | {10 // 3}")
    print(f"{LongInteger('-10') // LongInteger('3')} | {-10 // 3}")
    print(f"{LongInteger('10') % LongInteger('3')} | {10 % 3}")
    print(f"{LongInteger('-10') % LongInteger('3')} | {-10 % 3}")
    
    print(f"{LongInteger('-5') < LongInteger('0')} | {-5 < 0}")
    print(f"{LongInteger('100') > LongInteger('-100')} | {100 > -100}")
    print(f"{LongNatural('9' * 20) + LongNatural('1')} | {int('9' * 20) + 1}")
    print(f"{LongInteger('999999999999') * LongInteger('-111111111111')} | {999999999999 * (-111111111111)}")


    print(LongInteger("0") // LongInteger("0"))
