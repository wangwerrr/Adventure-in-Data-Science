def bubbleSort(array):
    # for each pass, we got biggest at the end which need no more comparison
    for passnum in range(len(array)-1, 0, -1):
        # for each iteration we start from the beginning, do comparison one by one
        for i in range(passnum):
            # swap two element if the order is incorrect
            if array[i] > array[i+1]:
            	array[i], array[i+1] = array[i+1], array[i]
            # else we just do nothing and continue to compare the following two elements
    return array    
