from random import random


def random_range(x1, x2) -> float:
    return (x2-x1)*random() + x1



class FloatMatrix:

    def _populate_array(self, shape, initial_range, depth=0):

        subdata = []
        size = shape[depth]

        if depth == len(shape)-1:
            for i in range(size):
                subdata.append(random_range(initial_range[0],initial_range[1]))
        else:
            for i in range(size):
                subdata.append(self._populate_array(shape, initial_range,depth+1))

        return subdata

    def _get_shape(self, array) -> 'list[int]':
        
        shape = []

        def parse_array(array):

            if isinstance(array, list):
                shape.append(len(array))
                parse_array(array[0])
            else:
                return
                
        return shape

    def __init__(self,shape : 'tuple[float]' = None, initial_range : 'tuple[float, float]' = (0,0), initial_data = None):
        
        if shape:
            self.shape = shape
            self.data = self._populate_array(shape,initial_range)
        elif initial_data:
            self.shape = self._get_shape(initial_data)
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
        
        # Recursively iterate over matrix values and multiply by scalar
        def pass_scalar_forward(array,scalar):

            for i,element in enumerate(array):

                if isinstance(element,list):
                    pass_scalar_forward(element, scalar)
                else:
                    array[i] = element*scalar

        copy = self.copy()
        pass_scalar_forward(copy.data,scalar)
        return copy

    def _return_mul_matrix(self, matrix : 'FloatMatrix') -> 'FloatMatrix':
        pass


    def __mul__(self, other) -> 'FloatMatrix':
        
        if isinstance(other,float) or isinstance(other,int):
            return self._return_mul_scalar(other)
        elif isinstance(other, self.__class__):
            pass
        else:
            print(f"TYPE ERROR : Can't multiply matrix by {other.__class__}")

# Tests
if __name__ == "__main__":

    test_matrix = FloatMatrix((2,2))
    print(test_matrix.data)
