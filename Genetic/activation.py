from math import e


def ReLU(x : float) -> float:
    return x if x > 0 else 0

def sigmoid(x : float) -> float:
    if x > 20:
        return 1
    elif x < -20:
        return 0
    
    return 1/(1+e**-x)

def LeakyReLU(x : float, epsilon : float = 0.2) -> float:
    return x if x >= 0 else x*epsilon

def tanh(x:float) -> float:
    if x > 20:
        return 1
    elif x < -20:
        return -1
    
    e2x = e**(2*x)
    return (e2x-1)/(e2x+1)


Activations = {

    "ReLU" : ReLU,
    "sigmoid" : sigmoid,
    "LeakyReLU" : LeakyReLU,
    "tanh" : tanh,

}


# Testing
if __name__ == "__main__":

    print("sigmoid(-1000)",sigmoid(-1000))
    print("sigmoid(4)",sigmoid(4))
    print("sigmoid(50)",sigmoid(50))
    print("sigmoid(-1)",sigmoid(-1))
    print("sigmoid(20)",sigmoid(20),'\n')

    print("tanh(-1000)",tanh(-1000))
    print("tanh(4)",tanh(4))
    print("tanh(50)",tanh(50))
    print("tanh(-1)",tanh(-1))
    print("tanh(1000)",tanh(1000))
    print("tanh(10)",tanh(10))