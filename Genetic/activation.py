from math import e



def ReLU(x : float) -> float:
    return x if x > 0 else 0

def sigmoid(x : float) -> float:
    if x > 30:
        return 1
    elif x < -30:
        return 0
    else: return 1/(1+e**-x)


Activations = {

    "ReLU" : ReLU,
    "sigmoid" : sigmoid,

}