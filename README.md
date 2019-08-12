# PVT-Tait-fitting
针对目前用经验方法建立的精度最高的修正双域Tait状态方程编写了拟合程序，实现了高分子材料PVT特性实验数据的拟合

# 修正双域 Tait PVT 模型数据拟合
修正双域Tait PVT模型可用于确定作为温度和压力的函数的材料密度。此变化可影响流动模拟的许多方面。修正双域 Tait pvT 模型可表示为以下方程：
ax^{2} + by^{2} + c = 0
$$\upsilon(T,p) = \upsilon_0(T)[1-Cln(1+\frac{p}{B(T)})]+\upsilon_t(T,p)$$
其中：<br>
&emsp;&emsp;$\upsilon(T,p)$ 是特定温度和压力下的体积比容<br>
&emsp;&emsp;$\upsilon_0$ 是零表压时的体积比容<br>
&emsp;&emsp;$T$ 为温度$(K)$<br>
&emsp;&emsp;$p$ 为压力$(Pa)$<br>
&emsp;&emsp;$C$ 为恒定值 0.0894 <br>
&emsp;&emsp;$B$ 表示材料的压力敏感度
$T_t$ 与压力的相关性可表示为一下方程： $T_t(p) = b_5 + b_6p$ &emsp;其中$b_5$（表示零表压时的体积转变温度$T_t$）和$b_6$是待拟合系数
在上方温度区域 $(T>T_t)$，<br>
&emsp;&emsp;$\upsilon_0 = b_{1m} + b_{2m}(T-b_5)$ <br>
&emsp;&emsp;$B(T) = b_{3m}e^{-b_{4m}(T-b_5)}$ <br>
&emsp;&emsp;$\upsilon_t(T, p) = 0$ <br>
&emsp;&emsp;其中，$b_{1m}、b_{2m}、b_{3m}$和$b_{4m}$是待拟合的系数<br><br>
在下方温度区域 $(T<T_t)$, <br>
&emsp;&emsp;$\upsilon_0 = b_{1s} + b_{2s}(T-b_5)$ <br>
&emsp;&emsp;$B(T) = b_{3s}e^{-b_{4s}(T-b_5)}$ <br>
&emsp;&emsp;$\upsilon_t(T, p) = b_7e^{b_8(T-b_5)-b_9p}$ <br>
&emsp;&emsp;其中，$b_{1s}、b_{2s}、b_{3s}、b_{4s}、b_7、b_8$和$b_9$是待拟合的系数 <br>
注意：晶体树脂的$\upsilon_t$值仅适用于低于转变温度的温度
