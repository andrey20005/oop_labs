use std::{cmp::Ordering, ops::{Add, Mul, Sub}};
use std::fmt;

#[derive(Clone, Debug)]
pub struct LongNatural {
    pub digits: Vec<u64>
}

impl LongNatural {
    pub fn from_u64(a: u64) -> LongNatural {
        return LongNatural { digits: vec![a] };
    }

    pub fn zero() -> LongNatural { return LongNatural { digits: vec![] };}

    fn is_zero(&self) -> bool {
        match self.digits.iter().max() {
            Some(m) => *m == 0u64,
            None => true
        }
    }
}

impl PartialEq for LongNatural {
    fn eq(&self, other: &Self) -> bool {
        self.digits == other.digits
    }
}

impl PartialOrd for LongNatural {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match self.digits.len().cmp(&other.digits.len()) {
            Ordering::Equal => {
                for i in (0..self.digits.len()).rev() {
                    match self.digits[i].cmp(&other.digits[i]) {
                        Ordering::Equal => continue,
                        other => return Some(other),
                    }
                }
                Some(Ordering::Equal)
            },
            other => Some(other),
        }
    }
}

impl Add<LongNatural> for LongNatural {
    type Output = LongNatural;

    fn add(self, rhs: LongNatural) -> Self::Output {
        let mut carry = false;
        let mut res = LongNatural::zero();
        for i in 0..self.digits.len().max(rhs.digits.len()) {
            let a = {
                if i >= self.digits.len() { 0u64 }
                else { self.digits[i] }
            };
            let b = {
                if i >= rhs.digits.len() { 0u64 }
                else { rhs.digits[i] }
            };
            let (sum, c_flag) = a.carrying_add(b, carry);
            carry = c_flag;
            res.digits.push(sum);
        }
        if carry { res.digits.push(1); }
        res
    }
}

impl Sub<LongNatural> for LongNatural {
    type Output = LongInteger;

    fn sub(mut self, mut rhs: LongNatural) -> Self::Output {
        if self == rhs { LongInteger::zero() }
        else {
            let mut res = LongInteger::zero();
            if self < rhs {
                res.sign = true;
                (self, rhs) = (rhs, self);
            }
            let mut borrow = false;
            for i in 0..self.digits.len().max(rhs.digits.len()) {
                let a = {
                    if i >= self.digits.len() { 0u64 }
                    else { self.digits[i] }
                };
                let b = {
                    if i >= rhs.digits.len() { 0u64 }
                    else { rhs.digits[i] }
                };
                let (diff, b_flag) = a.borrowing_sub(b, borrow);
                borrow = b_flag;
                res.abs.digits.push(diff);
            }
            while res.abs.digits.len() > 0 && res.abs.digits.last() == Some(&0) {
                res.abs.digits.pop();
            }
            res
        }
    }
}

impl Mul<u64> for LongNatural {
    type Output = LongNatural;
    fn mul(self, rhs: u64) -> Self::Output {
        let mut res = LongNatural::zero();
        let mut carry = 0u64;
        for i in 0..self.digits.len() {
            let prod = self.digits[i] as u128 * rhs as u128 + carry as u128;
            res.digits.push(prod as u64);
            carry = (prod >> 64) as u64;
        }
        if carry != 0 { res.digits.push(carry); }
        res
    }
}

impl Mul<LongNatural> for LongNatural {
    type Output = LongNatural;
    fn mul(self, rhs: LongNatural) -> Self::Output {
        if self.is_zero() || rhs.is_zero() {
            LongNatural::zero()
        }
        else if self.digits.len() == 1 { rhs * self.digits[0] }
        else if rhs.digits.len() == 1 { self * rhs.digits[0] }
        else {
            let n = (self.digits.len()/2).min(rhs.digits.len()/2);
            let a = LongNatural{digits: self.digits[0..n].to_vec()};
            let b = LongNatural{digits: self.digits[n..self.digits.len()].to_vec()};
            let c = LongNatural{digits: rhs.digits[0..n].to_vec()};
            let d = LongNatural{digits: rhs.digits[n..rhs.digits.len()].to_vec()};
            let ac = a.clone() * c.clone();
            let bd = b.clone() * d.clone();
            let chto_to = (((a + b) * (c + d) - ac.clone()).as_nat() - bd.clone()).as_nat();
            ac + 
            LongNatural{digits: [vec![0u64; n].as_slice(), chto_to.digits.as_slice()].concat()} +
            LongNatural{digits: [vec![0u64; n + n].as_slice(), bd.digits.as_slice()].concat()}
        }
    }
}

#[derive(Clone, Debug)]
pub struct LongInteger {
    pub sign: bool, // x < 0
    pub abs: LongNatural
}

impl LongInteger {
    pub fn from_i64(a: i64) -> LongInteger { 
        LongInteger { sign: a < 0, abs: LongNatural { digits: vec![a.abs() as u64] } }
    }

    pub fn from_u64(a: u64) -> LongInteger { 
        LongInteger { sign: false, abs: LongNatural { digits: vec![a] } }
    }

    pub fn zero() -> LongInteger { 
        LongInteger { sign: false, abs: LongNatural::zero() }
    }

    fn as_nat(self) -> LongNatural {
        self.abs
    }

    pub fn is_zero(&self) -> bool {
        return self.abs.is_zero();
    }
}

impl PartialEq for LongInteger {
    fn eq(&self, other: &Self) -> bool {
        self.sign == other.sign && self.abs == other.abs
    }
}

impl PartialOrd for LongInteger {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.sign && other.sign {
            match self.abs.partial_cmp(&other.abs) {
                Some(Ordering::Equal) => Some(Ordering::Equal),
                Some(Ordering::Greater) => Some(Ordering::Less),
                Some(Ordering::Less) => Some(Ordering::Greater),
                None => panic!("ytgjyznyj xnj")
            }
        } else if self.sign && !other.sign{
            Some(Ordering::Greater)
        } else if !self.sign && other.sign {
            Some(Ordering::Less)
        } else {
            self.abs.partial_cmp(&other.abs)
        }
    }
}

impl Sub<LongInteger> for LongInteger {
    type Output = Self;
    fn sub(self, rhs: LongInteger) -> Self::Output {
        if rhs.is_zero() {
            self
        } else {
            let rhs = LongInteger{sign: !rhs.sign, abs: rhs.abs};
            self + rhs
        }
    }
}

impl Add<LongInteger> for LongInteger {
    type Output = LongInteger;
    fn add(self, rhs: LongInteger) -> Self::Output {
        if self.sign == rhs.sign {
            LongInteger { sign: self.sign, abs: self.abs + rhs.abs }
        } else {
            let diff = self.abs - rhs.abs;
            LongInteger { sign: self.sign != diff.sign, abs: diff.abs }
        }
    }
}

impl Mul<LongInteger> for LongInteger {
    type Output = Self;
    fn mul(self, rhs: LongInteger) -> Self::Output {
        LongInteger{sign: self.sign != rhs.sign, abs: self.abs * rhs.abs}
    }
}

impl LongInteger {
    pub fn from_str(s: &str) -> Self {
        let mut res = LongInteger::zero();
        let mut sign = false;
        for c in s.chars() {
            if c == '-' {
                sign = true;
                continue;
            }
            res = res * LongInteger::from_u64(10);
            res = res + LongInteger::from_u64(match c {
                '0' => 0, '1' => 1, '2' => 2,
                '3' => 3, '4' => 4, '5' => 5,
                '6' => 6, '7' => 7, '8' => 8,
                '9' => 9,
                _ => 0
            });
        }
        res.sign = sign;
        res
    }
}

impl fmt::Display for LongInteger {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.sign && !self.abs.is_zero() {
            write!(f, "-")?;
        }
        if self.abs.is_zero() {
            return write!(f, "0");
        }
        let mut num = self.abs.clone();
        let mut digits:Vec<char> = vec![];
        while !num.is_zero() {
            let mut remainder = 0u64;
            for i in (0..num.digits.len()).rev() {
                let curr = ((remainder as u128) << 64) | (num.digits[i] as u128);
                
                num.digits[i] = (curr / 10) as u64;
                remainder = (curr % 10) as u64;
            }
            digits.push((b'0' + remainder as u8) as char);
            
            while num.digits.len() > 1 && num.digits.last() == Some(&0) {
                num.digits.pop();
            }
        }
        for c in digits.iter().rev() {
            write!(f, "{}", c)?;
        }
        Ok(())
    }
}

fn main() {
    println!("-168 * 12 = {}", LongInteger::from_str("-168") * LongInteger::from_str("12"));
    println!("-654 + 111 = {}", LongInteger::from_str("-654") + LongInteger::from_str("111"));
    println!(
        "-3453423423457089787866439985651166489951327 * 45245234342342396533651159864777511335888 = {}", 
        LongInteger::from_str("-3453423423457089787866439985651166489951327") * LongInteger::from_str("45245234342342396533651159864777511335888")
    );
    println!("10098995 + 2300000000000000000000000000000000000000000000000000000 = {}", LongInteger::from_str("10098995") + LongInteger::from_str("2300000000000000000000000000000000000000000000000000000"));
    println!("-100001 * -222222222222222222222222222222222222222222 = {}", LongInteger::from_str("-100001") * LongInteger::from_str("-222222222222222222222222222222222222222222"));
}
