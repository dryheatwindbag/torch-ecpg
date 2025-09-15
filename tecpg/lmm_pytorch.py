import torch
import numpy as np
import pandas as pd
from torchmin import minimize
from typing import Optional
from scipy.stats import t
from .config import get_device

def reml_log_likelihood(params, y, X, Z):
    """
    Calculates the REML log-likelihood for a linear mixed model.
    The optimizer will operate on the log of the variance components.
    """
    sigma2_e = torch.exp(params[0])
    sigma2_u = torch.exp(params[1])

    n = y.shape[0]

    # This assumes a simple random intercept model where Z is an identity matrix
    # of size n_samples x n_groups.
    # This is a simplification for the prototype. A more general implementation
    # would allow for more complex random effects structures.
    V = sigma2_u * (Z @ Z.T) + sigma2_e * torch.eye(n)
    V_inv = torch.inverse(V)

    # Profile out beta
    XtVinvX = X.T @ V_inv @ X
    XtVinvX_inv = torch.inverse(XtVinvX)
    beta_hat = XtVinvX_inv @ X.T @ V_inv @ y

    # REML log-likelihood formula
    log_det_V = torch.log(torch.det(V))
    log_det_XtVinvX = torch.log(torch.det(XtVinvX))

    y_minus_Xb = y - X @ beta_hat

    reml_ll = -0.5 * log_det_V - 0.5 * log_det_XtVinvX - 0.5 * y_minus_Xb.T @ V_inv @ y_minus_Xb

    return -reml_ll # Return negative for minimization

def lmm_pytorch_full(
    M: pd.DataFrame,
    G: pd.DataFrame,
    C: pd.DataFrame,
    Z: pd.DataFrame,
    M_annot: Optional[pd.DataFrame] = None,
    G_annot: Optional[pd.DataFrame] = None,
    region: str = 'all',
    window_base: Optional[int] = None,
    downstream: Optional[int] = None,
    upstream: Optional[int] = None,
    output_dir: Optional[str] = None,
    chunk_size: int = 0,
    **kwargs
):
    """
    Performs LMM analysis for each gene-methylation pair.
    """
    logger = kwargs.get('logger', None)
    device = get_device(**logger)

    n_samples = M.shape[1]
    Z = torch.tensor(Z.values, dtype=torch.float64).to(device)

    results = []

    pairs_to_test = []
    if region == 'all':
        for gene_id in G.index:
            for meth_id in M.index:
                pairs_to_test.append((gene_id, meth_id))
    else:
        if logger:
            logger.info('Initializing region filtration')

        G_annot_filtered = G_annot.reindex(G.index).dropna()
        M_annot_filtered = M_annot.reindex(M.index).dropna()

        for gene_id, g_annot_row in G_annot_filtered.iterrows():
            g_chrom = g_annot_row['chrom']
            g_pos = g_annot_row['chromStart']
            g_strand = g_annot_row['strand']

            for meth_id, m_annot_row in M_annot_filtered.iterrows():
                m_chrom = m_annot_row['chrom']
                m_pos = m_annot_row['chromStart']

                if region == 'trans' and g_chrom != m_chrom:
                    pairs_to_test.append((gene_id, meth_id))
                elif g_chrom == m_chrom:
                    if region == 'cis':
                        if g_strand == '+':
                            if g_pos - upstream < m_pos < g_pos + downstream:
                                pairs_to_test.append((gene_id, meth_id))
                        else:  # strand == '-'
                            if g_pos - downstream < m_pos < g_pos + upstream:
                                pairs_to_test.append((gene_id, meth_id))
                    elif region == 'distal':
                        # This is a simplified implementation of distal.
                        # The original implementation has window_base, upstream, and downstream.
                        # For now, we'll just consider anything outside the cis window as distal.
                        dist = abs(g_pos - m_pos)
                        if dist >= window_base:
                            pairs_to_test.append((gene_id, meth_id))

    if logger:
        logger.info(f"Found {len(pairs_to_test)} pairs to test after region filtration.")

    if chunk_size > 0:
        if output_dir is None:
            raise ValueError("Output directory must be specified when using chunking.")

        chunk_iterator = (pairs_to_test[i:i + chunk_size] for i in range(0, len(pairs_to_test), chunk_size))
        for i, chunk in enumerate(chunk_iterator):
            chunk_results = []
            for gene_id, meth_id in chunk:
                g_row = G.loc[gene_id]
                m_row = M.loc[meth_id]

                y = torch.tensor(g_row.values, dtype=torch.float64).to(device)

                X_np = np.hstack([
                    np.ones((n_samples, 1)),
                    m_row.values.reshape(-1, 1),
                    C.values
                ])
                X = torch.tensor(X_np, dtype=torch.float64).to(device)

                initial_params = torch.tensor([0.0, 0.0], dtype=torch.float64, requires_grad=True).to(device)

                result = minimize(
                    lambda params: reml_log_likelihood(params, y, X, Z),
                    initial_params,
                    method='l-bfgs',
                    disp=False
                )

                estimated_log_vars = result.x
                sigma2_e_est = torch.exp(estimated_log_vars[0])
                sigma2_u_est = torch.exp(estimated_log_vars[1])

                V_est = sigma2_u_est * (Z @ Z.T) + sigma2_e_est * torch.eye(y.shape[0])
                V_inv_est = torch.inverse(V_est)
                XtVinvX_est = X.T @ V_inv_est @ X
                XtVinvX_inv_est = torch.inverse(XtVinvX_est)
                beta_est = XtVinvX_inv_est @ X.T @ V_inv_est @ y

                chunk_results.append({
                    'gene_id': gene_id,
                    'meth_id': meth_id,
                    'beta_meth': beta_est[1].item(),
                    'sigma2_e': sigma2_e_est.item(),
                    'sigma2_u': sigma2_u_est.item()
                })

            chunk_df = pd.DataFrame(chunk_results)
            chunk_df.to_csv(f"{output_dir}/chunk_{i}.csv", index=False)
            if logger:
                logger.info(f"Saved chunk {i} to {output_dir}/chunk_{i}.csv")
        return None

    else:
        for gene_id, meth_id in pairs_to_test:
            g_row = G.loc[gene_id]
            m_row = M.loc[meth_id]

            if logger:
                logger.info(f"Running LMM for {gene_id} and {meth_id}")

            y = torch.tensor(g_row.values, dtype=torch.float64).to(device)

            # Construct the design matrix X for this pair
            # X includes an intercept, the methylation values, and covariates
            X_np = np.hstack([
                np.ones((n_samples, 1)),
                m_row.values.reshape(-1, 1),
                C.values
            ])
            X = torch.tensor(X_np, dtype=torch.float64).to(device)

            # Initial parameters for log-variances
            initial_params = torch.tensor([0.0, 0.0], dtype=torch.float64, requires_grad=True).to(device)

            # Minimize the negative REML log-likelihood
            result = minimize(
                lambda params: reml_log_likelihood(params, y, X, Z),
                initial_params,
                method='l-bfgs',
                disp=False
            )

            # Extract results
            estimated_log_vars = result.x
            sigma2_e_est = torch.exp(estimated_log_vars[0])
            sigma2_u_est = torch.exp(estimated_log_vars[1])

            # Calculate beta_hat with the final estimated variances
            V_est = sigma2_u_est * (Z @ Z.T) + sigma2_e_est * torch.eye(y.shape[0])
            V_inv_est = torch.inverse(V_est)
            XtVinvX_est = X.T @ V_inv_est @ X
            XtVinvX_inv_est = torch.inverse(XtVinvX_est)
            beta_est = XtVinvX_inv_est @ X.T @ V_inv_est @ y

            # Calculate standard errors and p-values
            hessian = torch.autograd.functional.hessian(
                lambda beta: reml_log_likelihood_beta(beta, y, X, Z, sigma2_e_est, sigma2_u_est),
                beta_est,
            )
            se = torch.sqrt(torch.diag(torch.inverse(hessian)))
            t_stats = beta_est / se
            p_values = 2 * t.sf(np.abs(t_stats.detach().numpy()), df=n_samples - X.shape[1])

            results.append({
                'gene_id': gene_id,
                'meth_id': meth_id,
                'beta_meth': beta_est[1].item(),
                'se_meth': se[1].item(),
                't_meth': t_stats[1].item(),
                'p_meth': p_values[1],
                'sigma2_e': sigma2_e_est.item(),
                'sigma2_u': sigma2_u_est.item()
            })

        return pd.DataFrame(results)

def reml_log_likelihood_beta(beta, y, X, Z, sigma2_e, sigma2_u):
    """
    Calculates the log-likelihood with respect to beta for the Hessian calculation.
    """
    n = y.shape[0]
    V = sigma2_u * (Z @ Z.T) + sigma2_e * torch.eye(n)
    V_inv = torch.inverse(V)

    XtVinvX = X.T @ V_inv @ X

    log_det_V = torch.log(torch.det(V))
    log_det_XtVinvX = torch.log(torch.det(XtVinvX))

    y_minus_Xb = y - X @ beta

    reml_ll = -0.5 * log_det_V - 0.5 * log_det_XtVinvX - 0.5 * y_minus_Xb.T @ V_inv @ y_minus_Xb

    return -reml_ll
