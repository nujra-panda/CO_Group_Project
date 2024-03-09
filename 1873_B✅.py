def inputt():
    numOfDig=int(input())
    lst = list(map(int,input().split()))
    return(lst)
def prodCalc(L):
    prodList=[]
    for i in range(0,len(L)):
        dumList=[]
        for l in range(0,len(L)):
            dum=L[l]
            dumList.append(dum)
        dumList[i]=dumList[i]+1
        dumProd=1
        for j in range(0,len(L)):
            dumProd=dumProd*dumList[j]
        prodList.append(dumProd)
    max=prodList[0]
    for i in range(0,len(prodList)):
        if(max<prodList[i]):
            max=prodList[i]
    return(max)
def main():
    n = int(input())
    finalresult=[]
    for i in range(0,n):   
        finalresult.append(prodCalc(inputt()))
    for i in finalresult:
        print(int(i))
main()
