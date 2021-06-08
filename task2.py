def summ(a,num):
    sum=0

    a = int(a)
    num =int(num)
    n = int(num/6)
    n1 = 3*n
    n2= 5*n


    if a == 1:
        i = 2
        j = n1
    if a == 2:
        i = n1
        j = n2
    if a == 0:
        i = n2
        j =num  # find start and end index: i,j

    for k in range(i,j):
        for m in range(2,k):
            if k % m == 0:
                break
        else:sum+=1   # sum for zhihshu


    return  sum   # return sum value


if __name__=='__main__':
    print(summ('2','20000'))