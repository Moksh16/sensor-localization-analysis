# KITTI EDA — Visualization Style Guide

## 1. Purpose

This document defines the visualization standards for the KITTI
sensor and localization exploratory data analysis project.

The objective is to ensure that all figures are readable, consistent,
and suitable for the project report and presentation.

## 2. Libraries

The following Python libraries are used:

- Matplotlib: figure creation, axes, labels, and saving plots.
- Seaborn: statistical plots, distributions, box plots, and heatmaps.
- Pandas: data preparation and grouping before visualization.

## 3. Figure Sizes and Resolution

The following figure sizes are used in the current notebook:

| Visualization | Figure size |
|---|---|
| Histograms and KDE | 8 x 5 inches |
| Box plots | 10 x 5 inches |
| Correlation heatmap | 18 x 15 inches |
| Pair plot | Seaborn-managed grid layout |

Figures are saved as PNG files at 300 DPI to provide sufficient
resolution for reports and presentations.

Tight layout and bounding-box adjustments are used where appropriate
to reduce clipping of titles, axis labels, and tick labels.

## 4. Colour Palette

### Distribution plots

Histograms and KDE plots use Seaborn's default colour settings.
The same settings are applied consistently across the distribution
plots.

### Box plots

Box plots use Seaborn's default colour settings to compare
measurements across driving sequences.

### Correlation heatmap

The correlation heatmap uses the RdBu_r diverging colour map.

- Blue represents negative correlation.
- White represents values near zero.
- Red represents positive correlation.

The scale is fixed between -1 and +1, with zero at the midpoint.
Correlation coefficients are displayed to two decimal places.

Note: The current heatmap uses RdBu_r instead of the originally
specified viridis palette because a diverging palette makes positive
and negative correlations easier to distinguish.

### Pair plot

The pair plot uses Seaborn's default styling, with semi-transparent
scatter points to reduce the visual impact of overlapping observations.

## 5. Titles, Fonts, and Labels

- Every figure should have a descriptive title.
- Every axis should have a meaningful label.
- Physical units should be included wherever applicable.
- Titles and labels should use clear, readable text.
- Tick labels should be rotated when necessary to avoid overlap.
- Numerical values should be rounded appropriately for readability.

Examples of units include metres per second (m/s) for velocity
components and degrees for latitude and longitude.

## 6. Figure File Naming

Figures are stored in the directory:

    eda/figures/

File names should describe their contents.

Examples:

- hist_kde_vf.png
- boxplot_vf_by_drive.png
- correlation_heatmap.png
- pairplot_position_orientation.png

Use descriptive, lowercase file names with underscores.

## 7. Data and Interpretation

- Driving sequences should be distinguished when comparing drives.
- Plots that combine multiple sequences must be interpreted carefully.
- Potential outliers should be investigated rather than automatically
  treated as errors.
- Correlation should not be interpreted as proof of causation.
- Categorical status codes should not automatically be treated as
  continuous numerical measurements.
- Conclusions should be based on the observed data and the limitations
  of the selected dataset.

## 8. Interactive Visualizations

The current deliverables use static PNG figures generated with
Matplotlib and Seaborn.

Interactive visualizations using Plotly may be added if they provide
additional value, such as hovering over individual observations to
inspect frame numbers, driving sequences, or measurement values.

Interactive plots are optional and are not required for the current
static-figure deliverables.

## 9. Output Organization

The expected directory structure is:

    eda/
        figures/
        visual_style.md

All figures should be saved in the figures directory, and this
document should remain in the eda directory.
