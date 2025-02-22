import matplotlib
matplotlib.use('agg')
import pylab as plt
import numpy as np

a = np.load("./lr_100.000000_more.npy")
b = np.load("./lr_10.000000_more.npy")
c = np.load("./lr_1.000000_more.npy")
d = np.load("./lr_0.100000_more.npy")
e = np.load("./lr_0.010000_more.npy")
#f = np.load("./lr_0.005000_more.npy")
#g = np.load("./lr_0.000500_more.npy")
#h = np.load("./lr_0.000050_more.npy")

#a = np.load("./lr_0.500000_more.npy")
xaxis=np.arange(1,10001)
print(a.shape,xaxis.shape)
#plt.plot(xaxis[20:],a[20:],b[20:],c[20:],d[20:])
#plt.plot(xaxis[100:],a[100:],b[100:],c[100:],d[100:],e[100:],f[100:],g[100:])
#plt.plot(xaxis[100:],a[100:],b[100:],c[100:],d[100:],e[100:],f[100:])
#plt.plot(xaxis[10000:20000],a[10000:20000],label='500')
print(a[0],b[0],c[0],d[0],e[0])
plt.plot(xaxis[:5],a[:5],label='100')
plt.plot(xaxis[:5] ,b[:5] ,label='10')
plt.plot(xaxis[:5] ,c[:5] ,label='1')
plt.plot(xaxis[:5] ,d[:5] ,label='0.1')
plt.plot(xaxis[:5] ,e[:5] ,label='0.01')
#plt.plot(xaxis ,f ,label='0.001')
#plt.plot(xaxis ,g ,label='0.0005')
#plt.plot(xaxis ,h ,label='0.00005')
'''
plt.plot(xaxis[1000:],a[1000:] ,label='100')
plt.plot(xaxis[1000:] ,b[1000:] ,label='10')
plt.plot(xaxis[1000:] ,c[1000:] ,label='1')
plt.plot(xaxis[1000:] ,d[1000:] ,label='0.1')
plt.plot(xaxis[1000:] ,e[1000:] ,label='0.01')
#plt.plot(xaxis ,f ,label='0.001')
#plt.plot(xaxis ,g ,label='0.0005')
#plt.plot(xaxis ,h ,label='0.00005')
'''

plt.xlabel("Iteration")
plt.ylabel("loss")
plt.title("Compare different learning rate with adagrad")
plt.legend()
plt.grid(True)
plt.savefig('lr_compare_ada_test.jpg')
