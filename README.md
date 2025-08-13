# Portfolio Risk Analysis Dashboard

## Overview
This Streamlit application provides an interactive dashboard for analyzing portfolio **risk metrics** across different business units and departments. The tool allows users to visualize relationships between key financial indicators through scatter plots and combined bar-line charts.

## Key Features

### 1. Interactive Scatter Plot Visualization
- **Multi-sheet selection:** Combine data from different Excel sheets (`TOTAL CARTERA_resumen`, `PRIMERA COMPRA_resumen`, `RECOMPRA_resumen`).
- **Business unit filtering:** Compare metrics across **EL BODEGON**, **LA MARINA**, and **PROGRESSA**.
- **Dynamic filtering:**
  - Loan terms (1–60 months or "All")
  - Departments/products (with minimum portfolio threshold of 550,000)
- **Customizable axes:**
  - X-axis options: USGAAP 90/60 weighted percentages, RRR, margin, active rate
  - Y-axis options: Same as X-axis (multiple selection allowed)
- **Visual enhancements:**
  - Color-coded by business unit
  - Bubble sizes scaled by total portfolio capital
  - Interactive hover information
- **Download filtered data capability**

### 2. Combined Bar-Line Chart
- Visualizes **RRR (Return on Risk Ratio)** alongside **USGAAP 90 delinquency percentage**.
- **Features:**
  - Business unit selection
  - Loan term filtering
  - Automatic grouping when "All" terms selected
  - Minimum portfolio threshold of 100,000
  - Value labels on bars
  - Dual y-axes for different metrics

## Technical Implementation

### Data Processing
- Loads data from `Resumen_Cartera_Morosidad.xlsx` with multiple sheets
- Applies weighted averages when grouping data
- Filters include:
  - Minimum delinquency threshold (30%)
  - Positive portfolio capital
  - Interest rate products only
  - Department ID exclusions (60xxx)

### Visualization Tools
- **Plotly** for interactive charts
- **Seaborn** for styling
- **Streamlit** for web interface

### Color Scheme
Custom color variants for each business unit:
- **EL BODEGON:** Red variants
- **LA MARINA:** Green variants
- **PROGRESSA:** Purple variants

## Usage Instructions
1. Select data sheets to include
2. Choose business units for comparison
3. Set filters (loan term, departments)
4. Configure chart axes
5. Interact with visualizations:
   - Hover for details
   - Zoom/pan
   - Download filtered data

For the bar-line chart:
1. Select data sheet
2. Choose business unit
3. Set loan term filter

## Requirements
- Python 3.x
- Streamlit
- Pandas
- Plotly
- Seaborn
- Matplotlib

## To run:
```bash
streamlit run grafica.py
```

---
This README is written in Markdown and is ready to be used on platforms like GitHub, GitLab, or documentation generators.
