import numpy as np
from simpleNet import layers
from simpleNet.layers.other_conv2d import Conv2d_other


conv = layers.Conv2D(2, 3, 2, padding="valid", bias=False)
x = np.random.rand(10, 2, 2, 2).astype(np.float64)
epsilon = 1e-7


def my_loss(y_pred):
    return np.sum(y_pred)


def my_loss_back(y_pred):
    return np.ones(y_pred.shape)


# grad
z = conv(x)
l = my_loss(z)
dz = my_loss_back(z)
conv.backwards(dz)

grad = conv.cached_grad["w"].copy()

# 计算gradapprox
w = np.copy(conv.weights["w"])
gradapprox = np.zeros(w.shape, dtype=np.float64)

_, W, H = w.shape

for i in range(W):
    for j in range(H):
        # weight + - ，再算 J- J+
        conv.weights["w"][0, i, j] += epsilon
        z = conv(x)
        J_plus = my_loss(z)
        conv.weights["w"][0, i, j] -= 2*epsilon
        z = conv(x)
        J_minus = my_loss(z)

        gradapprox[0, i, j] = (J_plus - J_minus) / (2 * epsilon)
        conv.weights["w"][0, i, j] += epsilon

# gradapprox /= 12
# 结果
numerator = np.linalg.norm(grad - gradapprox)
denominator = np.linalg.norm(gradapprox) + np.linalg.norm(grad)
diff = numerator / denominator

print(grad.shape)
print(gradapprox.shape)
print(diff)