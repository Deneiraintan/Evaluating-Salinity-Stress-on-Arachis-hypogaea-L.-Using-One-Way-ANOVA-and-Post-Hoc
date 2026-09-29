# Evaluating-Salinity-Stress-on-Arachis-hypogaea-L.-Using-One-Way-ANOVA-and-Post-Hoc-in-Python
This script simulates experimental crop data under NaCl stress constraints and executes an automated One-Way ANOVA &amp; Post-Hoc Tukey HSD pipeline.
# 🔬 Stunted Growth Analytics: Evaluating Salinity Stress on Arachis hypogaea L. Using-One-Way-ANOVA-and-Post-Hoc-in-Python

## 📌 Project Overview
This repository serves as an open-source reproducibility package for investigating the morphological and physiological impacts of climate-driven salinity stress on glycophyte crop models, specifically **Peanut (*Arachis hypogaea* L.)**. 

This research project bridges large-scale ecological crises—such as peatland drainage and estuarine seawater intrusion in Central Kalimantan—with controlled, randomized laboratory simulations. The analytical framework utilizes **inferential biostatistics** (One-Way ANOVA and Tukey's Honest Significant Difference) implemented via Python to determine the exact threshold where saline irrigation severely hinders crop development and dry biomass allocation.

---

## 📂 Repository Structure
- `data/peanut_salinity_data.csv`: Synthetic experimental raw dataset calibrated based on real-world biological distributions.
- `scripts/salinity_inferential_test.py`: Production-ready Python script executing EDA, automated One-Way ANOVA, and Post-Hoc Tukey HSD testing.
- `output/salinity_stress_boxplot.png`: High-resolution data visualizations generated automatically by the visualization pipeline.

---

## 📈 Statistical Workflow & Key Insights
1. **Exploratory Data Analysis (EDA):** Visualized distribution variances using seaborn-derived boxplots to cross-examine physiological metrics.
2. **Inferential Modeling (ANOVA):** The One-Way ANOVA confirmed a highly significant constraint (p < 0.01) of NaCl levels on both plant height and dry weight, mirroring empirical wet-lab conditions.
3. **Post-Hoc Pairwise Testing:** Tukey's HSD test revealed that even a low salinity threshold (**25 mM NaCl**) triggers immediate osmotic shock, resulting in a statistically significant drop in dry biomass compared to the control group (p-adj < 0.05).
4. **Data Engineering Constraints:** Integrated a value-clipping safeguard within the conditional data loop to ensure absolute physical properties remain biologically sound (>0) while preserving high-variance profiles for stress-testing.

---

## 📚 References
- Mawaddah, S., Hemon, A. F., & Aryana, I. G. (2026). Uji Toleransi pada Fase Kecambah Beberapa Genotipe Kacang Tanah (Arachis hypogaea L.) terhadap Cekaman Salinitas . Jurnal Ilmiah Mahasiswa , 201-209.
- Perwira, J., Hermantio, F. Y., Nusantara, E. T., Dhani, M. I., Bezaleel, Y. A., Falahudhin, S. W., & Hafidhoh, U. N. (2022). Pengaruh Cekaman Salinitas terhadap Pertumbuhan Kacang Tanah (Arachis hypogaea L.). Jurnal Penelitian Universitas Brawijaya, 1-6.
- Satu, S. I., Mansora, & Ahmad, S. (2019). Effects of Salinity on the Growth and Development of Groundnut PlANT (Arachis hypogaea L.). Journal of Bangladesh Academy of Sciences, 25-30.
- Yunita, R., Khumaida, N., Sopandie, D., & Mariska, I. (2018). Analisis Cekaman Salinitas terhadap Padi Mutan pada Kondisi In Vitro. Penelitian Pertanian Tanaman Pangan, 25-34.
