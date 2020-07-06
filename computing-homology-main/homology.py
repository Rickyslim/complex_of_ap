import numpy
import numpy.linalg
import matlab.engine
import scipy.io as sio
class ComputeBettiNumber():
#复形的前两位贝蒂数计算
   @staticmethod
   def rowSwap(A, i, j):
      temp = numpy.copy(A[i, :])
      A[i, :] = A[j, :]
      A[j, :] = temp
   @staticmethod
   def colSwap(A, i, j):
      temp = numpy.copy(A[:, i])
      A[:, i] = A[:, j]
      A[:, j] = temp
   @staticmethod
   def scaleCol(A, i, c):
      A[:, i] *= c*numpy.ones(A.shape[0])
   @staticmethod
   def scaleRow(A, i, c):
      A[i, :] *= c*numpy.ones(A.shape[1])
   @staticmethod
   def colCombine(A, addTo, scaleCol, scaleAmt):
      A[:, addTo] += scaleAmt * A[:, scaleCol]
   @staticmethod
   def rowCombine(A, addTo, scaleRow, scaleAmt):
      A[addTo, :] += scaleAmt * A[scaleRow, :]
   @staticmethod
   def simultaneousReduce(A, B):
      if A.shape[1] != B.shape[0]:
         raise Exception("Matrices have the wrong shape.")

      numRows, numCols = A.shape

      i,j = 0,0
      while True:
         if i >= numRows or j >= numCols:
            break

         if A[i,j] == 0:
            nonzeroCol = j
            while nonzeroCol < numCols and A[i,nonzeroCol] == 0:
               nonzeroCol += 1

            if nonzeroCol == numCols:
               i += 1
               continue

            ComputeBettiNumber.colSwap(A, j, nonzeroCol)
            ComputeBettiNumber.rowSwap(B, j, nonzeroCol)

         pivot = A[i,j]
         ComputeBettiNumber.scaleCol(A, j, 1.0 / pivot)
         ComputeBettiNumber.scaleRow(B, j, 1.0 / pivot)

         for otherCol in range(0, numCols):
            if otherCol == j:
               continue
            if A[i, otherCol] != 0:
               scaleAmt = -A[i, otherCol]
               ComputeBettiNumber.colCombine(A, otherCol, j, scaleAmt)
               ComputeBettiNumber.rowCombine(B, j, otherCol, -scaleAmt)

         i += 1; j+= 1

      return A,B

   @staticmethod
   def finishRowReducing(B):
      numRows, numCols = B.shape

      i,j = 0,0
      while True:
         if i >= numRows or j >= numCols:
            break

         if B[i, j] == 0:
            nonzeroRow = i
            while nonzeroRow < numRows and B[nonzeroRow, j] == 0:
               nonzeroRow += 1

            if nonzeroRow == numRows:
               j += 1
               continue

            ComputeBettiNumber.rowSwap(B, i, nonzeroRow)

         pivot = B[i, j]
         ComputeBettiNumber.scaleRow(B, i, 1.0 / pivot)

         for otherRow in range(0, numRows):
            if otherRow == i:
               continue
            if B[otherRow, j] != 0:
               scaleAmt = -B[otherRow, j]
               ComputeBettiNumber.rowCombine(B, otherRow, i, scaleAmt)

         i += 1; j+= 1

      return B

   @staticmethod
   def numPivotCols(A):
      z = numpy.zeros(A.shape[0])
      return [numpy.all(A[:, j] == z) for j in range(A.shape[1])].count(False)

   @staticmethod
   def numPivotRows(A):
      z = numpy.zeros(A.shape[1])
      return [numpy.all(A[i, :] == z) for i in range(A.shape[0])].count(False)

   @staticmethod
   def bettiNumber(d_k, d_kplus1):
      A, B = numpy.copy(d_k), numpy.copy(d_kplus1)
      ComputeBettiNumber.simultaneousReduce(A, B)
      ComputeBettiNumber.finishRowReducing(B)

      dimKChains = A.shape[1]
      # print(dimKChains,"K阶链群维度")
      kernelDim = dimKChains - ComputeBettiNumber.numPivotCols(A)
      # print(kernelDim,"kernel维度")
      imageDim = ComputeBettiNumber.numPivotRows(B)
      # print(imageDim,"image空间维度")

      return kernelDim - imageDim

# matrix_first_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_first.mat'
# matrix_first=sio.loadmat(matrix_first_mat)
# matrix_second_mat=u'D:/1Learning/江苏大学/覆盖问题/复形/复形/results/matrix_second.mat'
# matrix_second=sio.loadmat(matrix_second_mat)
# matrix_zero=numpy.zeros((1,45))
# print("————————————————————————The 1st and 2nd Betti Numbers are:————————————————————")
# print("——————0th homology: %d" % ComputeBettiNumber.bettiNumber(matrix_zero.astype('float'),matrix_first["matrix_first"].astype('float')))
# print("——————1st homology: %d" % ComputeBettiNumber.bettiNumber(matrix_first["matrix_first"].astype('float'),matrix_second["matrix_second"].astype('float')))
