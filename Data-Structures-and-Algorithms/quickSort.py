def quickSort(array):
    helper(array, 0, len(array)-1)
    return array
    
# Recursion
def helper(array, first, last): # need first & last index as func argument
    if first >= last:
        return
    else:
        splitpoint = partition(array, first, last)
        
        helper(array, first, splitpoint-1)
        helper(array, splitpoint+1, last)
        
# Partition Operation: put pivotvalue into right place; return the index (splitpoint)
def partition(array, first, last):
    pivotvalue = array[first]
    
    leftmark = first + 1
    rightmark = last
    
    done = False
    while not done:
        while leftmark <= rightmark and array[leftmark] <= pivotvalue:
            leftmark += 1
        while rightmark >= leftmark and array[rightmark] >= pivotvalue:
            rightmark -= 1
        if rightmark < leftmark:
            done=True
        else:
            # swap rightmark element with leftmark element
            array[leftmark], array[rightmark] = array[rightmark], array[leftmark] 
            
    # swap rightmark element with pivot element(which is the first element)
    array[first], array[rightmark] = array[rightmark], array[first]
    
    # return pivot index (which equals to the rightmark after partition)
    return rightmark
    

test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
print quicksort(test)
