f=open('./d.txt','r',encoding='gbk')
d=''.join(f.read())
f.close()
d+='//'
for i in range(1000):
          d+='hello'
f=open('./d.txt','w',encoding='gbk')
f.write(d)
f.close()

