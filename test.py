
def sortByValue(inputValue):
    criteria = ((320-inputValue[0])**2 + (240-inputValue[1])**2)**0.5
    return criteria


sortList = [[3, 1], [4, 6], [0, 1], [245, 0], [244, 100]]
sortList.sort(key=sortByValue)
print(sortList)
