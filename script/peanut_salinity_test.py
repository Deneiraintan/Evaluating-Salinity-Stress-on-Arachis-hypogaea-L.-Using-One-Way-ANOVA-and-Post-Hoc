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
# 1. EXPERIMENTAL DATA SYNTHESIS & CLEANING
# ==============================================================================
# Lock randomness seed to ensure consistent data structures on runtime execution
np.random.seed(42)

# Define the number of pot replications per treatment group
replications = 5

# Register salt concentration levels (experimental treatments)
treatments = ['0 mM', '25 mM', '50 mM', '75 mM', '100 mM']
data_list = []

# Nested loop pipeline: Process each treatment then generate 5 independent pots
for t in treatments:
    for rep in range(replications):
        
        # Configure mean value parameters (loc) for Height and Biomass based on real trends
        if t == '0 mM':
            height = np.random.normal(loc=5.8, scale=0.6)
            biomass = np.random.normal(loc=21.8, scale=1.5)
        elif t == '25 mM':
            height = np.random.normal(loc=0.02, scale=0.4)
            biomass = np.random.normal(loc=16.2, scale=1.2)
        elif t == '50 mM':
            height = np.random.normal(loc=-0.32, scale=0.3)
            biomass = np.random.normal(loc=11.8, scale=1.0)
        elif t == '75 mM':
            height = np.random.normal(loc=0.68, scale=0.4)
            biomass = np.random.normal(loc=10.5, scale=0.9)
        else: # 100 mM
            height = np.random.normal(loc=1.18, scale=0.5)
            biomass = np.random.normal(loc=15.2, scale=1.3)
            
        # Non-significant (ns) environmental variables -> Uniform mean across all pots
        leaf_area = np.random.normal(loc=4.5, scale=1.1)
        chlorophyll = np.random.normal(loc=0.5, scale=0.1)
        carotenoid = np.random.normal(loc=0.3, scale=0.08)
        
        # Append structured row metrics into the data collection basket
        data_list.append([t, height, leaf_area, biomass, chlorophyll, carotenoid])

# Convert data matrix into a structured Pandas DataFrame object
columns = ['Treatment', 'Plant_Height', 'Leaf_Area', 'Biomass', 'Chlorophyll', 'Carotenoids']
df_botany = pd.DataFrame(data_list, columns=columns)

# Data cleaning pipeline based on biological logic criteria
df_cleaned = df_botany[(df_botany['Leaf_Area'] > 0) & (df_botany['Biomass'] > 0)]

# Automatically export processed data to target path directory
df_cleaned.to_csv('../data/peanut_salinity_data.csv', index=False)
print("[DATA EXPORT] Processed dataset successfully saved to 'data/peanut_salinity_data.csv'\n")

# ==============================================================================
# 2. AUTOMATED STATISTICAL PIPELINE (ANOVA & TUKEY'S HSD)
# ==============================================================================
print("=== MULTI-PARAMETRIC QUALITY ASSURANCE AUDIT ===")
variables_to_test = ['Plant_Height', 'Leaf_Area', 'Biomass', 'Chlorophyll', 'Carotenoids']

for var in variables_to_test:
    # Compute the ordinary least squares (OLS) ANOVA model formula for each variable
    formula = f"{var} ~ C(Treatment)"
    model = ols(formula, data=df_cleaned).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    # Extract the distinct P-Value metric from the salt treatment factor row
    p_value = anova_table.loc['C(Treatment)', 'PR(>F)']
    status = "SIGNIFICANT (**)" if p_value < 0.05 else "NOT SIGNIFICANT (ns)"
    
    print(f"\n[AUDIT] Variable: {var}")
    print(f" -> P-Value: {p_value:.6f} | Status: {status}")
    
    # Trigger Post-Hoc Tukey HSD analysis evaluation only for significant features
    if p_value < 0.05:
        tukey = pairwise_tukeyhsd(endog=df_cleaned[var], groups=df_cleaned['Treatment'], alpha=0.05)
        print(f" --- Post-Hoc BNJ Table Summary (Top 3 Interactions) ---")
        
        # Convert summary outputs into a clean Pandas DataFrame for refined terminal logs
        tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
        print(tukey_df.head(3))

# ==============================================================================
# 3. HIGH-RESOLUTION SEABORN VISUALIZATION
# ==============================================================================
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Plant Physiological Response Under Salinity Stress Constraints', fontsize=18, fontweight='bold')

axes_flat = axes.flatten()

# Automated plotting loop to generate distinct boxplots per analytical feature
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

# Drop the empty 6th subplot frame to maintain a balanced layout symmetry
fig.delaxes(axes_flat[-1])
plt.tight_layout()

# Save final graphical publication figure plot inside results folder path
plt.savefig('../results/salinity_stress_boxplot.png', dpi=300)
print("[VISUALIZATION SUCCESS] Figure saved as 'results/salinity_stress_boxplot.png'")
