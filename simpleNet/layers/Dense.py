import numpy as np
from simpleNet.layers.Layer import Layer


class Dense(Layer):

    def __init__(self, input_num: int, hidden_num: int, use_bias: bool = True):
        super().__init__()
        self.name = "Dense"
        self.hidden_num = hidden_num
        self.use_bias = use_bias

        w = np.random.rand(input_num, self.hidden_num).astype(np.float32)
        self.weights = {"w":w}
        if self.use_bias:
            b = np.random.rand(self.hidden_num).astype(np.float32)
            self.weights["b"] = b

    def __call__(self, *args, **kwargs):
        # forward
        x = args[0]
        self.cached_x = x # 备用
        if self.use_bias:
            w, b = self.weights["w"], self.weights["b"]
            z = np.matmul(x, w) + b
        else:
            w = self.weights["w"]
            z = np.matmul(x, w)
        return z

    def backwards(self, da):
        x = self.cached_x
        m = da.shape[0]
        dw = x.transpose().dot(da) / m
        self.cached_grad = {"w": dw}
        if self.use_bias:
            db = np.sum(da, axis=0) / m
            self.cached_grad["b"] = db
        w_T = self.weights["w"].transpose()
        a_prev = np.matmul(da, w_T)
        return a_prev

    def __str__(self):
        return "%s: " % self.name + "hidden_num: %d, " % self.hidden_num + "use_Bias: %s" % str(self.use_bias)
