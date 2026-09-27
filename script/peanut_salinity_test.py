"""
Project Title: Evaluating Salinity Stress on Arachis hypogaea L. Using Inferential Biostatistics
Author: Deneira Intan Pitaloka
Description: This script simulates experimental crop data under NaCl stress constraints
             and executes an automated One-Way ANOVA & Post-Hoc Tukey HSD pipeline.
             Customized pathway pathways for: data/ and results/ directories.
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. EXPERIMENTAL DATA SYNTHESIS & SEED LOCKING
# ==============================================================================
# Locking randomness to guarantee reproducibility across different environments
np.random.seed(42)

replications = 5
treatments = ['0 mM', '25 mM', '50 mM', '75 mM', '100 mM']
data_list = []

# Nested loop: Iterating through each treatment to construct 5 biological replications
for t in treatments:
    for rep in range(replications):
        
        # Calibration of mean distribution vectors based on empirical laboratory trends
        if t == '0 mM':
            height = np.random.normal(loc=5.8, scale=0.6)
            biomass = np.random.normal(loc=21.8, scale=1.5)
        elif t == '25 mM':
            height = np.random.normal(loc=2.2, scale=0.4)  
            biomass = np.random.normal(loc=16.2, scale=1.2)
        elif t == '50 mM':
            height = np.random.normal(loc=1.1, scale=0.3)   
            biomass = np.random.normal(loc=11.8, scale=1.0)
        elif t == '75 mM':
            height = np.random.normal(loc=0.68, scale=0.4)
            biomass = np.random.normal(loc=10.5, scale=0.9)
        else:  # 100 mM
            height = np.random.normal(loc=0.5, scale=0.2)   
            biomass = np.random.normal(loc=6.4, scale=0.8)   
            
        # DATA ENGINEERING CONSTRAINT (Data Integrity Guard):
        # Preventing absolute physical metrics from generating non-biological negative numbers
        height = max(0.01, height)
        biomass = max(0.01, biomass)
        
        # Non-significant variables (ns) -> Uniformly calibrated across all distributions
        leaf_area = np.random.normal(loc=4.5, scale=1.1)
        chlorophyll = np.random.normal(loc=0.5, scale=0.1)
        carotenoid = np.random.normal(loc=0.3, scale=0.08)
        
        data_list.append([t, height, leaf_area, biomass, chlorophyll, carotenoid])

# Converting data matrix into a structured Pandas DataFrame
columns = ['Treatment', 'Plant_Height', 'Leaf_Area', 'Biomass', 'Chlorophyll', 'Carotenoids']
df_botany = pd.DataFrame(data_list, columns=columns)

# Data Cleaning Pipeline
df_cleaned = df_botany[(df_botany['Leaf_Area'] > 0) & (df_botany['Biomass'] > 0)]
print(f"[SUCCESS] Synthetic dataset generated and cleaned. Total samples: {len(df_cleaned)} rows.\n")

# Exporting raw data automatically into the data/ directory
df_cleaned.to_csv('../data/peanut_salinity_data.csv', index=False)
print("[DATA EXPORT] Raw data successfully saved to 'data/peanut_salinity_data.csv'\n")

# ==============================================================================
# 2. AUTOMATED LOOP FOR ANOVA & POST-HOC (TUKEY'S HSD)
# ==============================================================================
print("=== MULTI-PARAMETRIC QUALITY ASSURANCE AUDIT ===")
variables_to_test = ['Plant_Height', 'Leaf_Area', 'Biomass', 'Chlorophyll', 'Carotenoids']

for var in variables_to_test:
    # Compute ANOVA model formula for each variable
    formula = f"{var} ~ C(Treatment)"
    model = ols(formula, data=df_cleaned).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    # Extracting P-Value specifically on the treatment factor row
    p_value = anova_table.loc['C(Treatment)', 'PR(>F)']
    status = "SIGNIFICANT (**)" if p_value < 0.05 else "NOT SIGNIFICANT (ns)"
    
    print(f"\n[AUDIT] Variable: {var}")
    print(f" -> P-Value: {p_value:.6f} | Status: {status}")
    
    # Conditional Post-Hoc Tukey HSD (Executed only if the ANOVA yields a significant effect)
    if p_value < 0.05:
        tukey = pairwise_tukeyhsd(endog=df_cleaned[var], groups=df_cleaned['Treatment'], alpha=0.05)
        print(f" --- Post-Hoc Tukey HSD Table Summary ---")
        
        # Formatting Tukey summary matrix into a readable Pandas DataFrame object
        tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
        print(tukey_df.head(3))

# ==============================================================================
# 3. HIGH-RESOLUTION DATA VISUALIZATION
# ==============================================================================
print("\n" + "="*50)
print("[VISUALIZATION] Generating high-resolution publication plots...")

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Plant Physiological Response Under Salinity Stress Constraints', fontsize=18, fontweight='bold')

axes_flat = axes.flatten()

# Automated loop generation for Seaborn Boxplots across metrics
for i, var in enumerate(variables_to_test):
    sns.boxplot(
        ax=axes_flat[i],
        data=df_cleaned,
        x='Treatment',
        y=var,
        palette='viridis',  
        hue='Treatment',
        legend=False
    )
    axes_flat[i].set_title(f'Distribution of {var}', fontsize=12, fontweight='semibold')
    axes_flat[i].set_xlabel('Salt Concentration', fontsize=10)
    axes_flat[i].set_ylabel('Measured Value', fontsize=10)

# Removing the empty 6th subplot layout for structural symmetry
fig.delaxes(axes_flat[-1])
plt.tight_layout()

# Saving publication-ready figure directly into the results/ directory
plt.savefig('../results/salinity_stress_boxplot.png', dpi=300)
print("[VISUALIZATION SUCCESS] Figure saved as 'results/salinity_stress_boxplot.png'")
