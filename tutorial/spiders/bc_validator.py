from hashlib import sha256
import sys
import pdb

import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58decode(v, length):
  """ decode v into a string of len bytes
"""
  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += __b58chars.find(c) * (__b58base**i)

  result = ''
  while long_value >= 256:
    div, mod = divmod(long_value, 256)
    result = chr(mod) + result
    long_value = div
  result = chr(long_value) + result

  nPad = 0
  for c in v:
    if c == __b58chars[0]: nPad += 1
    else: break

  result = chr(0)*nPad + result
  if length is not None and len(result) != length:
    return None

  return result
 
def check_bc(bc):
    bcbytes = b58decode(bc, 25)
    if not bcbytes:
        return False
    if bcbytes == True:
        return True
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
 
if __name__ == '__main__':
    bc = '1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i'
    assert check_bc(bc)
    assert not check_bc( bc.replace('N', 'P', 1) )
    assert check_bc('1111111111111111111114oLvT2')
    assert check_bc("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j")

