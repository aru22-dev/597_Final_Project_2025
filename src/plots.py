import numpy as np
import matplotlib.pyplot as plt
import os

def ensure_figures_dir():
    if not os.path.exists("figures"):
        os.makedirs("figures")

# H1 PLOT: BAR CHART OF TOTAL INFECTIONS
def plot_h1(mean_individual, mean_household):
    ensure_figures_dir()

    labels = ["Individual Isolation", "Household Isolation"]
    values = [mean_individual, mean_household]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values, color=["#5DADE2", "#48C9B0"])
    plt.ylabel("Mean Total Infections")
    plt.title("H1: Isolation Strategy Comparison")

    plt.savefig("figures/h1_isolation_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()


# H2 PLOT: PEAK DAY & PEAK LOAD
def plot_h2(peak_day_high, peak_day_low, peak_I_high, peak_I_low):
    ensure_figures_dir()

    #PEAK DAY COMPARISON
    plt.figure(figsize=(6,4))
    labels = ["High Contacts", "Low Contacts"]
    values = [peak_day_high, peak_day_low]

    plt.bar(labels, values, color=["#F1948A", "#BB8FCE"])
    plt.ylabel("Mean Peak Day")
    plt.title("H2: Outbreak Peak Timing")

    plt.savefig("figures/h2_peak_day.png", dpi=300, bbox_inches="tight")
    plt.close()

    #PEAK LOAD COMPARISON
    plt.figure(figsize=(6,4))
    values = [peak_I_high, peak_I_low]

    plt.bar(labels, values, color=["#F5B041", "#52BE80"])
    plt.ylabel("Mean Peak Infectious Count")
    plt.title("H2: Peak Caseload Comparison")

    plt.savefig("figures/h2_peak_load.png", dpi=300, bbox_inches="tight")
    plt.close()


# H3 PLOT: PROBABILITY OF LARGE OUTBREAK
def plot_h3(prob_no_vax, prob_vax):
    ensure_figures_dir()

    labels = ["No Vaccination", "30% Vaccination"]
    values = [prob_no_vax, prob_vax]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values, color=["#EC7063", "#7DCEA0"])
    plt.ylabel("P(Large Outbreak)")
    plt.title("H3: Probability of Major Outbreak")

    plt.savefig("figures/h3_probability.png", dpi=300, bbox_inches="tight")
    plt.close()

