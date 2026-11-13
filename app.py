# import packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Setup the Streamlit page layout
st.set_page_config(page_title="AAF Dynamics Simulator", layout="wide")
st.title("Alternate Allele Frequencies (AAF) Simulator")
st.write("Adjust the Strain A frequency below to see how the distribution shifts.")

# 2. Create the Streamlit slider
# Streamlit will automatically update the variable and rerun the script when this changes
strain_A_ratio = st.slider(
    "Strain A %:", 
    min_value=0.01, 
    max_value=0.99, 
    value=0.50, 
    step=0.01
)

# 3. Core Simulation Logic
np.random.seed(42)
n_sites = 10000
depth = 30
strain_B_ratio = 1 - strain_A_ratio
sites_different = 6000

n_sites_A = sites_different // 2 
alt_sites_A = np.random.binomial(n=depth, p=strain_A_ratio, size=n_sites_A)

n_sites_B = sites_different // 2 
alt_sites_B = np.random.binomial(n=depth, p=strain_B_ratio, size=n_sites_B)

n_sites_ref = (n_sites - n_sites_B - n_sites_A) // 2
alt_sites_ref = np.random.binomial(n=depth, p=.05, size=n_sites_ref)
alt_sites_ref[alt_sites_ref > 1] = 1

remaining_sites = n_sites - n_sites_B - n_sites_A - n_sites_ref 
alt_sites_alt = np.random.binomial(n=depth, p=.95, size=remaining_sites)
alt_sites_alt[alt_sites_alt > depth] = depth

alt_depth = np.concatenate((alt_sites_A, alt_sites_B, alt_sites_ref, alt_sites_alt))

site_source = (
    ["sites_A"] * len(alt_sites_A)
    + ["sites_B"] * len(alt_sites_B)
    + ["sites_ref"] * len(alt_sites_ref)
    + ["sites_alt"] * len(alt_sites_alt)
)

ref_depth = depth - alt_depth
sites = [f"Site_{i}" for i in range(1, n_sites + 1)]

df = pd.DataFrame({
    'site': sites,
    'site_source': site_source,
    'REF_depth': ref_depth,
    'ALT_depth': alt_depth
})

df['ALT_frequency'] = df['ALT_depth'] / (df['REF_depth'] + df['ALT_depth'])

# 4. Plotting
# We create the figure exactly as before
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

ax1.hist(df["ALT_frequency"].dropna(), bins=15, range=(0, 1), color="steelblue", edgecolor="lightsteelblue")
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0, 3000) 
ax1.set_title(f"Distribution of Alternate Allele Frequencies (A: {strain_A_ratio:.2f})", fontsize=14)
ax1.set_xlabel("Alternate Allele Frequency", fontsize=12)
ax1.set_ylabel("Number of Sites", fontsize=12)

source_order = ["sites_A", "sites_B", "sites_ref", "sites_alt"]
source_frequencies = [df.loc[df["site_source"] == source, "ALT_frequency"].dropna() for source in source_order]
source_colors = ["tab:blue", "tab:purple", "tab:green", "tab:grey"]

ax2.hist(
    source_frequencies, bins=15, range=(0, 1), stacked=True,
    color=source_colors, edgecolor="white", label=source_order
)

ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0, 3000) 
ax2.set_title("Alternate Allele Frequencies by Site Source", fontsize=14)
ax2.set_xlabel('Alternate Allele Frequency', fontsize=12)
ax2.set_ylabel('Number of Sites', fontsize=12)
ax2.legend(title="Site source")

# 5. Display the plot in Streamlit
st.pyplot(fig)