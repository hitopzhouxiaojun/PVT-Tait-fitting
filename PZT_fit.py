#----------------------- 需要提供的基础数据 ------------------------------------
import numpy as np
import matplotlib.pyplot as plt
#plt.rcParams['figure.figsize'] = (7.5, 6)
from scipy import optimize
import pandas as pd
np.seterr(divide='ignore',invalid='ignore')

# 需要先把实验原始数据做一个单位换算，统一换成国际单位
point_info = pd.read_csv('test.csv',index_col='T')/1e6

# 用于计算b5，确定每个压力值下的Tt
Tt_Test = np.array([565, 570, 575, 582, 585])
p = np.array([0.1,50,100,150,180])*1e6

# 初始值的设定，初始值的选取非常重要
init = [0.0006151, 5.205e-7, 1.498e8, 0.0134, 
        0.0005951,6.026e-8,2.00511e8, 2.886e-7, 2.003e-5, 0.0759, 1.197e-8]
# b1m, b2m, b3m, b4m
# b1s, b2s, b3s, b4s, b7, b8, b9
#bounds = [(2e-6, 0.2), (1e-9, 0.0001),(5e5,5e10),(1e-7,1)]

# 变量数、数据点数目：用于计算R方
var_num = 11
point_num = 65

#----------------------- 数据可视化 -------------------------------------------
def data_visual(point_info):
    c=['b', 'g', 'r', 'c', 'k']
    for i,column in enumerate(point_info.columns):
        plt.plot(point_info[column],'%so--' %c[i],label="%s MPa" %column)
    plt.legend()
    plt.xlabel('Temperature (K)')
    plt.ylabel('Specific volume ($m^3$/kg)')
    plt.title('PVT curves')
    plt.grid(linestyle='--', which='both')
    plt.show()
data_visual(point_info)

# ----------------------- 计算Tt/b5--------------------------------------------
def func(p, b5, b6):
    return  b5 + b6 *p

def comput_b5(Tt, p):
    [b5, b6], _ = optimize.curve_fit(func, p, Tt)    
    return b5, b6

def show_b5(b5, b6,p,Tt):
    fitx = np.linspace(1e6,180e6,10)
    plt.plot(p/1e6,Tt,'o--', label="Test")
    plt.plot(fitx/1e6, func(fitx, b5, b6), label="Fit")
    plt.legend()
    plt.xlabel('Pressure (MPa)\n$b_5$=%s; $b_6$=%.3e'%(round(b5,3), b6))
    plt.ylabel('Temperature (K)')
    plt.title('$T_t$-Pressure')
    plt.show()  

b5, b6 = comput_b5(Tt_Test, p)
show_b5(b5, b6,p,Tt_Test)
Tt = func(p, b5, b6)
[b5, b6]

#-------------------------拟合--------------------------------------------
data_up = point_info.copy()

# 分温度区间计算拟合值
def comput_fit(x, pressure, b5, t, i):
    b1m, b2m, b3m, b4m, b1s, b2s, b3s, b4s, b7, b8, b9=x
    if t > Tt[i]:
        res = (b1m+b2m*(t-b5))*(1-0.0894*np.log(1+pressure/(b3m*np.exp(-b4m*(t-b5)))))
    else:
        res = (b1s+b2s*(t-b5))*(1-0.0894*np.log(1+pressure/(b3s*np.exp(-b4s*(t-b5)))))+b7*np.exp(b8*(t-b5)-b9*pressure)
    return res

# 在给定拟合参数的情况下，计算拟合的均方差
def func_fit(x, *args):
    b1m, b2m, b3m, b4m, b1s, b2s, b3s, b4s, b7, b8, b9=x
    b5, = args
    e = 0
    for i, column in enumerate(data_up.columns):
        series = data_up[column]
        pressure = float(column)*1e6
        for t,v in series.items():
            vol = comput_fit(x, pressure, b5, t, i)
            e += (v-vol)**2
    return e**0.5

res_fit = optimize.minimize(func_fit, init, args=(b5,), method="nelder-mead", options={'disp': True, 'maxfev': 3000*5})
#options={'xtol': 1e-12, 'disp': True}   constraints=con_up()    tol=1e-10
res_fit.x

#-------------------------拟合效果展示--------------------------------------------
def compute_fit(res_up):
    for i, column in enumerate(data_fit.columns):
        pressure = float(column)*1e6
        for t,v in data_fit[column].items():
            data_fit[column][t] = comput_fit(res_up, pressure, b5, t, i)

data_fit = point_info.copy()
compute_fit(res_fit.x)

c=['b', 'g', 'r', 'c', 'k']
for i,column in enumerate(point_info.columns):
    plt.plot(point_info[column],'%so--' %c[i],label="%s MPa" %column)
plt.legend()

for i,column in enumerate(data_fit.columns):
    plt.plot(data_fit[column],'%s' %c[i])
    
#-------------------------拟合结果评估/R-adj--------------------------------------------
mean = np.mean(point_info.mean())
R_square = 1-sum(((data_fit-point_info)**2).sum())/sum(((point_info-mean)**2).sum())
R_adj = 1-(1-R_square**2)*(point_num-1)/(point_num-var_num-1)
print('R_square:%s\nR_adj:%s' %(R_square, R_adj))

temp_str1 = '$b_{1m}$=%.3e; $b_{2m}$=%.3e; $b_{3m}$=%.3e; $b_{4m}$=%.3e' % (res_fit.x[0],res_fit.x[1],res_fit.x[2],res_fit.x[3])
temp_str2 = '$b_{1s}$=%.3e; $b_{2s}$=%.3e; $b_{3s}$=%.3e; $b_{4s}$=%.3e' % (res_fit.x[4],res_fit.x[5],res_fit.x[6],res_fit.x[7])
temp_str3 = '$b_7$=%.3e; $b_8$=%.3e; $b_9$=%.3e' % (res_fit.x[8],res_fit.x[9],res_fit.x[10])
temp_str4 = 'R_square=%.3f; R_adj=%.3f' % (R_square,R_adj)
plt.xlabel('Temperature (K)\n%s\n%s\n%s\n%s'%(temp_str1, temp_str2, temp_str3, temp_str4))
plt.ylabel('Specific volume ($m^3$/kg)')
plt.title('PVT curves')
plt.show()

#-------------------------拟合结果评估/误差百分比--------------------------------------------
error = (data_fit-point_info)/point_info*100
error
