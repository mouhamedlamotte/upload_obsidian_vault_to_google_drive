import os

def compare_properties(object1 , object2):
    """
    Compare the properties of two files or directories
    """

    print(os.stat(object1))
    print(os.stat(object2))


    return os.stat(object1) == os.stat(object2)
