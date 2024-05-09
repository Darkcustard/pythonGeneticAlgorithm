from random import random


def random_range(x1, x2) -> float:
    return (x2-x1)*random() + x1



class FloatMatrix:

    def __init__(self,shape : tuple[float], initial_range : tuple[float, float] = (0,0), initial_data = None):

        self.shape = shape

        # Recursively populate array
        def populate_array(shape, depth=0):

            subdata = []
            size = shape[depth]

            if depth == len(shape)-1:
                for i in range(size):
                    subdata.append(random_range(initial_range[0],initial_range[1]))
            else:
                for i in range(size):
                    subdata.append(populate_array(shape, depth+1))

            return subdata
        
        # Initialize values
        self.data = populate_array(shape)

        if initial_data:
            self.data = initial_data

    def copy(self) -> 'FloatMatrix':

        def copy_row(row) -> list:
            
            copied_row = []

            for item in row:
                if isinstance(item,list):
                    copied_row.append(copy_row(item))
                else:
                    copied_row.append(item)

            return copied_row
        
        copied_data = copy_row(self.data)
        return FloatMatrix(self.shape, initial_data=copied_data)
            
            
        

    def _return_mul_scalar(self, scalar : float) -> 'FloatMatrix':
        pass

    def _return_mul_matrix(self, matrix : 'FloatMatrix') -> 'FloatMatrix':
        pass


    def __mul__(self, other):
        
        if isinstance(other,float) or isinstance(other,int):
            pass
        elif isinstance(other, self.__class__):
            pass

# Tests
if __name__ == "__main__":

    # Shape Test
    print("Expecting 8 Values")
    test_matrix = FloatMatrix([2,2,2], (0,10))
    print(test_matrix.data)
    
    print("Linear : ")
    for z in test_matrix.data:
        for y in z:
            for x in y:
                print(x)

    test_matrix*1
    test_matrix*FloatMatrix((2,),(0,1))


    print("COPYING TRUE IF CORRECT")
    copied_matrix = test_matrix.copy()
    print(copied_matrix.data==test_matrix.data)
