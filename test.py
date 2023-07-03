import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建一个高斯分布的粒子分布
mu = [0, 0, 0]  # 均值
sigma = [1, 1, 1]  # 标准差
num_particles = 1000  # 粒子数量

particles = np.random.normal(mu, sigma, (num_particles, 3))

# 绘制正方体
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 正方体的八个顶点
# 正方体的八个顶点
vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1]
])

# 正方体的六个面
faces = np.array([
    [0, 1, 3, 2],
    [0, 1, 5, 4],
    [0, 2, 6, 4],
    [1, 3, 7, 5],
    [2, 3, 7, 6],
    [4, 5, 7, 6]
])

# 绘制正方体
for face in faces:
    ax.add_collection3d(plt.Polygon(vertices[face]))

# 绘制粒子分布
ax.scatter(particles[:, 0], particles[:, 1], particles[:, 2], c='r', marker='o')

# 设置坐标轴范围
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图形
plt.show()