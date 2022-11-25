''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Matrix.py
  - Implementation of 4D vectors and
    matrix and algebraic operations
    between them.
  
  Last modified (yy-mm-dd): 2022-09-12
--------------------------------------
'''

from functools import reduce

# ----- Objetos

class V4:
  '''Vector 4D'''
  def __init__(self, array:list):
    self.matrix = array
  
  def __repr__(self) -> str:
    return f'V4:\n{self.matrix}\n'

  def __matmul__(self, other):
    '''Multiplication with 4x4 matrix'''
    if type(other) == M4:
      return matrixMul(
        M4([[ x for x in self.matrix ]]),
        other
      )

class M4:
  '''4x4 Matrix'''
  def __init__(self, array:list):
    self.matrix = array
  
  def __repr__(self) -> str:
    return f'M4:\n{self.matrix}\n'\
    
  def __matmul__(self, other):
    '''Multiplication of matrixes'''
    if type(other) == M4:
      return matrixMul(self, other)
    
    '''Multiplication with 4D vector'''
    if type(other) == V4:
      return transpos(
        matrixMul(
          self, 
          M4([ [x] for x in other.matrix ])
        )
      )

# ----- Operaciones de Algebra Lineal

def transpos(M:M4) -> M4:
  '''Returns the transposed matrix of M'''
  return M4([[ x[0] for x in M.matrix ]])

def matrixMul(M1:M4, M2:M4) -> M4:
  '''Returns the multiplication between M1 and M2'''
  M1, M2 = M1.matrix, M2.matrix
  n1 = len(M1[0])
  n2 = len(M2)

  if n1 != n2: raise Exception('Invalid Sizes of matrixes', n1, n2)
  m = len(M1)
  n = len(M2[0])

  return M4 ([
    [
      reduce(
        lambda last, next: last + next, 
        [ M1[i][k] * M2[k][j] for k in range(n1) ]
      ) for j in range(n)
    ] for i in range(m)
  ])