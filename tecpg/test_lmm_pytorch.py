import unittest
import pandas as pd
import numpy as np
from tecpg.lmm_pytorch import lmm_pytorch_full
from tecpg.test_data import generate_lmm_data
from tecpg.logger import Logger

class TestLmmPytorch(unittest.TestCase):
    def test_lmm_pytorch_full(self):
        beta_true = [1.5, 2.5, 0.5, -0.5]
        sigma2_e_true = 1.0
        sigma2_u_true = 1.5
        M, G, C, Z, M_annot, G_annot = generate_lmm_data(
            n_samples=100,
            n_meth_rows=10,
            n_gene_rows=10,
            n_groups=10,
            n_covariates=2,
            beta_true=beta_true,
            sigma2_e_true=sigma2_e_true,
            sigma2_u_true=sigma2_u_true,
            annotation=True,
        )

        # For this test, we'll only test one pair to keep it fast.
        G = G.iloc[[0]]
        M = M.iloc[[0]]

        logger = Logger()
        result_df = lmm_pytorch_full(M, G, C, Z, logger=logger)

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn('beta_meth', result_df.columns)

        # Check if the estimated beta is reasonably close to the true value
        self.assertAlmostEqual(result_df['beta_meth'].iloc[0], beta_true[1], delta=0.5)
        self.assertAlmostEqual(result_df['sigma2_e'].iloc[0], sigma2_e_true, delta=0.5)
        self.assertAlmostEqual(result_df['sigma2_u'].iloc[0], sigma2_u_true, delta=0.6)

if __name__ == '__main__':
    unittest.main()
