# class hello:
# #     def hello(self):
# #         print("hi")
# #
# # class hello2(hello):
# #     pass
# #
# # x=hello2()
# # x.hello()

# x=list(map(int,input().split(" ")))
#
# n, T = list(map(int, input().split(" ")))
# x = []
# for i in range(n):
#     s, t = list(map(int, input().split(" ")))
#     if t <= T:
#         x.append(s)
#
# if len(x) == 0:
#     print("TLE")
# else:
#     print(min(x))
import numpy as np

x=np.random.random()

x=np.zeros((2,2))
x=np.append(x,[2])
print(x.flatten())

def a():
    return np.append(x,3)
print(a())
print(x)
x=[str(int(k)) for k in x]
s=''.join(x)
print(s)