from random import random

def randrange(x1,x2) -> float:
    return (x2-x1)*random()+x1

def is_number(x : str) -> bool:
    if len(x) == 0: return False
    digits = list("0123456789.")
    return sum([1 if char in digits else 0 for char in x]) == len(x)

def is_int(x : float) -> bool:
    return round(x)==x

class FloatMatrix:

    def __init__(self, shape : 'list[int,int]' = [2,2], initial_range : 'list[int,int]' = [-1,1], initial_data : 'list' = None ):

        if initial_data:
            self.data = initial_data
            self.shape = [len(self.data), len(self.data[0])]
        else:
            self.shape = shape
            self.data = [[randrange(initial_range[0], initial_range[1]) for i in range(self.shape[1]) ] for i in range(self.shape[0])]

    def copy(self) -> 'FloatMatrix':
        data = []
        for row in self.data:
            data.append(row.copy())
        return FloatMatrix(initial_data = data)


    # Method overloading
    def __str__(self):
        return '\n'.join([str(self.data[i]) for i in range(len(self.data))])

    def __mul__(self, other) -> 'FloatMatrix':

        # Scalar 
        if isinstance(other,int) or isinstance(other, float):
            copy = self.copy()
            for row in copy.data:
                for i in range(len(row)):
                    row[i] = row[i]*other

            return copy

        # Matrix multiplication
        elif isinstance(other,self.__class__):

            data = [[0 for x in range(other.shape[1])] for y in range(self.shape[0])]
            for row in range(self.shape[0]):
                for col in range(other.shape[1]):
                    for k in range(self.shape[1]):
                        data[row][col] += self.data[row][k]*other.data[k][row]
                        
            return FloatMatrix(initial_data=data)

        # Undefined
        else:
            print(f"TYPE ERROR: undefined behaviour : Matrix * {other.__class__}")
            exit()

# Testing
if __name__ == "__main__":

    print("-------------------------------------\nENTERING FUNCTION TESTING MODE...\n-------------------------------------")
    x1, x2 = (-10, 20)
    print("\nRandrange:")
    print(f"Range : {x1,x2}")
    [print(randrange(x1,x2)) for i in range(5)]

    print("\nIs number:")
    print("''", is_number(''))
    print("'5000'", is_number('5000'))
    print("'120.5'", is_number('120.5'))
    print("'.9999'", is_number('.9999'))
    print("'0.500abcd'", is_number('0.555abcd'))
    print("'3.1415'", is_number('3.1415'))


    print("-------------------------------------\nENTERING FLOATMATRIX TESTING MODE...\n-------------------------------------")
    print("Scalar multiplication :\n")

    print("Matrix : ")
    test = FloatMatrix(initial_data=[[1,1,1],[1,1,1],[1,1,1]])
    print(test)

    scalar = round(random()*10)
    print(f"\nScalar : \n{scalar}")


    print("\nResultant : ")
    product = test*scalar
    print(product)

    print("Matrix Multiplication :\n")

    print("Matrix 1: ")
    test1 = FloatMatrix(initial_data=[[1,2,3]])
    print(test1)

    print("\nMatrix 2: ")
    test2 = FloatMatrix(initial_data=[[1,1,1],[2,2,2],[3,3,3]])
    print(test2)

    product = test1*test2
    print("\nProduct :")
    print(product)
    


