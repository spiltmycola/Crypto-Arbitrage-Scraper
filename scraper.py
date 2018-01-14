import bs4 as bs
import urllib.request
import json

source = urllib.request.urlopen("https://coinmarketcap.com/currencies/bitcoin/#markets")
soup = bs.BeautifulSoup(source, 'lxml')
jsonout = open("db.json","w")

table = soup.find('table', {'id':'markets-table'})
rows = table.find_all('tr')[1:]

uniquePairs = []

priceDict = {
    'pairs':[]
}

''' Creating list of Unique Pairs '''
for row in rows:
    pair = row.find_all('a')[1].text
    new = True
    for uniquePair in uniquePairs:
        if pair == uniquePair:
            new = False
    if new:
        uniquePairs.append(pair)

''' Finding lowest and highest price for each pair '''
for uniquePair in uniquePairs:
    first = True
    highest = 0
    lowest = 10e+10
    lowestExchange = 'placeholder'
    highestExchange = 'placeholder'
    for row in rows:
        links = row.find_all('a')
        curPair = links[1].text
        if curPair == uniquePair:
            curExchange = links[0].text
            price = float(row.find('span', {'class':'price'}).get('data-native'))
            if price < lowest:
                lowest = price
                lowestExchange = curExchange
            if price > highest:
                highest = price
                highestExchange = curExchange
    percentDiff = (highest - lowest)/lowest * 100
    priceDict['pairs'].append({
        'pair': uniquePair,
        'lowest': {
            'value': lowest,
            'exchange': lowestExchange
        },
        'highest': {
            'value': highest,
            'exchange': highestExchange
        },
        'percentDiff': percentDiff
    })

''' Sorting '''

''' mergeSort Function '''
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i]['percentDiff'] < righthalf[j]['percentDiff']:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

''' Sort call '''
mergeSort(priceDict['pairs'])
priceDict['pairs'].reverse()

jsonout.write(json.dumps(priceDict))