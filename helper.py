# all coefficients are in UAH
BFa = 20  # base fare
CPMin = 4  # cost per minute
CPkm = 12  # cost per kilometer
SBM = 1.1  # surge boost multiplier
BFe = 5  # booking fare


def min_max(dicti, time):
    if len(dicti) == 1:
        return dicti
    if time:
        sorted_by_time = {k: v for k, v in sorted(dicti.items(), key=lambda item: item[1][0])}
        return min_max(dict(list(sorted_by_time.items())[:(len(sorted_by_time) // 2)]), False)
    else:
        sorted_by_length = {k: v for k, v in sorted(dicti.items(), key=lambda item: item[1][1])}
        return min_max(dict(list(sorted_by_length.items())[:(len(sorted_by_length) // 2)]), True)
