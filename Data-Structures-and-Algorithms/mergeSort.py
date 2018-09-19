def mergeSort(array):
    if len(array) <= 1:
        return
    else:
        # split
        mid = len(array)//2
        lefthalf = array[:mid]  # space complexity O(n)
        righthalf = array[mid:]
        
        mergeSort(lefthalf)
        mergeSort(righthalf)
        
        # merge
        i, j, k = 0, 0, 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
	            array[k] = lefthalf[i]
                i += 1
            else:
                array[k] = righthalf[j]
                j += 1
            k += 1
        while i < len(lefthalf):
            array[k] = lefthalf[i]
            i += 1
            k += 1
        while j < len(righthalf):
            array[k] = righthalf[j]
            j += 1
            k += 1
