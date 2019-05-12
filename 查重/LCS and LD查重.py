def lcs(a,b):
     lena=len(a)
     lenb=len(b)
     c=[[0 for i in range(lenb+1)] for j in range(lena+1)]
     flag=[[0 for i in range(lenb+1)] for j in range(lena+1)]
     for i in range(lena):
          for j in range(lenb):
               if a[i]==b[j]:
                    c[i+1][j+1]=c[i][j]+1
                    flag[i+1][j+1]='ok'
               elif c[i+1][j]>c[i][j+1]:
                    c[i+1][j+1]=c[i+1][j]
                    flag[i+1][j+1]='left'
               else:
                    c[i+1][j+1]=c[i][j+1]
                    flag[i+1][j+1]='up'
     return c,flag
def getLcs(flag,a,b):
    global res
    res=''
    def printLcs(flag,a,i,j):
            global res
            if i==0 or j==0:
                    return
            if flag[i][j]=='ok':
                    printLcs(flag,a,i-1,j-1)
                    res+=a[i-1]
            elif flag[i][j]=='left':
                    printLcs(flag,a,i,j-1)
            else:
                    printLcs(flag,a,i-1,j)
    printLcs(flag,a,len(a),len(b))
    return res
def TransformString(A,B):
        m=len(A)
        n=len(B)
        c=[[0 for j in range(n+1)]for i in range(m+1)]
        for i in range(m+1):
                c[i][0]=i
        for j in range(n+1):
                c[0][j]=j
        for i in range(1,m+1):
                for j in range(1,n+1):
                        c[i][j]=min(c[i-1][j]+1,c[i][j-1]+1,c[i-1][j-1]+int(A[i-1]!=B[j-1]))
        return c[m][n]
f1=open('./stopwords.txt', 'r', encoding='gbk')
f2=open('./a.txt','r',encoding='gbk')
f3=open('./b.txt','r',encoding='gbk')
stopwords =f1.read().split('\n')[:-1]
a1=f2.read().split('\n')[:-1]
a=[]
for item in a1:#去除注释
     a.append(item.split('//')[0])
a=''.join(a)
b1=f3.read().split('\n')[:-1]
b=[]
for item in b1:#去除注释
     b.append(item.split('//')[0])
b=''.join(b)
f1.close()
f2.close()
f3.close()
a=''.join(a.split( ))#去除空格
b=''.join(b.split( ))#去除空格
for item in stopwords:#去除无关字符
        if item in a:
                a=''.join(a.split(item))
        if item in b:
                b=''.join(b.split(item))
print(a)
print(b)
print(len(a))
print(len(b))
c,flag=lcs(a,b)
Lcs=c[len(a)][len(b)]
#M=getLcs(flag,a,b)
#print(M)
ts=TransformString(a,b)
print("基于LCS和编辑距离重复率为:%.2f%%"%(Lcs/(ts+Lcs)*100))
