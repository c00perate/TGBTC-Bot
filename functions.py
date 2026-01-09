def sort(arr, sortingby):
    n = len(arr)
    for i in range(n - 1):
        minIndex = i

        for j in range(i+1, n):
            if arr[j][sortingby] > arr[minIndex][sortingby]:
                minIndex = j

        arr[i], arr[minIndex] = arr[minIndex], arr[i]

