def merge_sort(events_list, key, ascending=True):

    if not events_list:
        return []

    data_copy = events_list.copy()
    mergesort2(data_copy, 0, len(data_copy) - 1, key, ascending)
    return data_copy


def mergesort2(S, low, high, key, ascending):
    if low < high:
        mid = (low + high) // 2
        mergesort2(S, low, mid, key, ascending)
        mergesort2(S, mid + 1, high, key, ascending)
        merge2(S, low, mid, high, key, ascending)


def merge2(S, low, mid, high, key, ascending):
    R = []
    i, j = low, mid + 1

    while i <= mid and j <= high:
        cond = (S[i][key] <= S[j][key]) if ascending else (S[i][key] >= S[j][key])
        if cond:
            R.append(S[i])
            i += 1
        else:
            R.append(S[j])
            j += 1

    if i > mid:
        for k in range(j, high + 1):
            R.append(S[k])
    else:
        for k in range(i, mid + 1):
            R.append(S[k])

    for k in range(len(R)):
        S[low + k] = R[k]


def binary_search(events_list, target_name):

    sorted_data = merge_sort(events_list, key="name", ascending=True)
    low = 0
    high = len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_data[mid]["name"].lower()
        target = target_name.lower()

        if mid_name == target:
            return sorted_data[mid]
        elif mid_name > target:
            high = mid - 1
        else:
            low = mid + 1

    return None


def sort_by_price(events_list, ascending=True):
    return merge_sort(events_list, key="price", ascending=ascending)


def sort_by_duration(events_list, ascending=True):
    return merge_sort(events_list, key="duration", ascending=ascending)
