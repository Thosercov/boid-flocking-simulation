from math import sqrt

def calculate_hypotenuse(vector):
    return sqrt(vector[0] ** 2 + vector[1] ** 2)

def get_distance(vec1, vec2):
    return  min(abs(calculate_hypotenuse(vec1)),abs(calculate_hypotenuse(vec2)))


        

