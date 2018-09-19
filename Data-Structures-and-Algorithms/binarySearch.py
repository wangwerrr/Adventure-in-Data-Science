def binarySearch(input_array, value):
    low = 0
    up = len(input_array) -1
    
    while low <= up:  
        mid = (up + low)//2  # choose left element as mid for even length array
        if value == input_array[mid]:
            return mid
        elif value > input_array[mid]:
            low = mid +1
        else:
            up = mid - 1
    return -1
