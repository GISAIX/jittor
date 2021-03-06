
# ***************************************************************
# Copyright (c) 2020 Jittor. Authors: 
#     Wenyang Zhou <576825820@qq.com>
#     Dun Liang <randonlang@gmail.com>. 
# All Rights Reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import unittest
import jittor as jt
import numpy as np
import jittor.nn as jnn

skip_this_test = False

try:
    jt.dirty_fix_pytorch_runtime_error()
    import torch
    import torch.nn as tnn
except:
    torch = None
    tnn = None
    skip_this_test = True

def check_equal(arr, j_layer, p_layer, is_train=True, threshold=1e-5):
    jittor_arr = jt.array(arr)
    pytorch_arr = torch.Tensor(arr)
    if is_train:
        assert np.allclose(p_layer.running_mean.detach().numpy(), j_layer.running_mean.numpy(), threshold)
        assert np.allclose(p_layer.running_var.detach().numpy(), j_layer.running_var.numpy(), threshold)
    else:
        assert np.allclose(p_layer.layer.running_mean.detach().numpy(), j_layer.running_mean.numpy(), threshold)
        assert np.allclose(p_layer.layer.running_var.detach().numpy(), j_layer.running_var.numpy(), threshold)
    jittor_result = j_layer(jittor_arr)
    pytorch_result = p_layer(pytorch_arr)
    if is_train:
        assert np.allclose(p_layer.running_mean.detach().numpy(), j_layer.running_mean.numpy(), threshold)
        assert np.allclose(p_layer.running_var.detach().numpy(), j_layer.running_var.numpy(), threshold)
    else:
        assert np.allclose(p_layer.layer.running_mean.detach().numpy(), j_layer.running_mean.numpy(), threshold)
        assert np.allclose(p_layer.layer.running_var.detach().numpy(), j_layer.running_var.numpy(), threshold)
    assert np.allclose(pytorch_result.detach().numpy(), jittor_result.numpy(), threshold)

@unittest.skipIf(skip_this_test, "No Torch found")
class TestBatchNorm(unittest.TestCase):
    def test_batchnorm(self):
        # ***************************************************************
        # Test BatchNorm Layer
        # ***************************************************************
        arr = np.random.randn(16,10,224,224)
        check_equal(arr, jnn.BatchNorm(10, is_train=True), tnn.BatchNorm2d(10))

        class Model(tnn.Module):
            def __init__(self):
                super(Model, self).__init__()
                self.layer = tnn.BatchNorm2d(10)
            def forward(self, x):
                return self.layer(x)
        model = Model()
        model.eval()
        check_equal(arr, jnn.BatchNorm(10, is_train=False), model, False)
        

if __name__ == "__main__":
    unittest.main()