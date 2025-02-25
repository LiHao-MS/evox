import unittest
from functools import partial

import torch

from evox.core import vmap


@partial(vmap)
def _single_eval(x: torch.Tensor, p: float = 2.0, q: torch.Tensor = torch.tensor([0, 1])):
    return (x**p).sum() * q.sum()


class TestJitUtil(unittest.TestCase):
    def setUp(self):
        self.expected = torch.tensor([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])

    def test_single_eval(self):
        result = _single_eval(2 * torch.ones(10, 2))
        self.assertTrue(torch.equal(result, self.expected))

    def test_jit_single_eval(self):
        result = torch.compile(_single_eval)(2 * torch.ones(10, 2))
        self.assertTrue(torch.equal(result, self.expected))

    def test_jit_single_eval_trace_lazy(self):
        result = torch.compile(_single_eval)(2 * torch.ones(10, 2))
        self.assertTrue(torch.equal(result, self.expected))
