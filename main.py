from src.data_processing import load_malawi_contacts, split_into_days, daily_edge_lists
from src.analysis_h1 import run_h1
from src.analysis_h2 import run_h2
from src.analysis_h3 import run_h3
from src.plots import plot_h1, plot_h2, plot_h3

def main():
    df = load_malawi_contacts("data/malawi_contacts.csv")
    days = split_into_days(df)
    edges = daily_edge_lists(days)

    # H1 config & run
    mean_individual, mean_household, reduction_h1 = run_h1(
        edges,
        num_days=120,
        num_runs=100,
        infection_prob=0.03,
        infectious_days=5,
        external_infection_prob=0.001,
        initial_infected=3,
    )

    # H2 config & run
    (
        mean_peak_day_high,
        mean_peak_day_low,
        mean_peak_I_high,
        mean_peak_I_low,
        delay_h2,
        reduction_peak_h2,
    ) = run_h2(
        edges,
        num_days=120,
        num_runs=200,
        infection_prob=0.08,
        infectious_days=5,
        external_infection_prob=0.001,
        initial_infected=3,
        contact_reduction_low=0.4,
        min_attack=0.2,
    )

    # H3 config & run
    p_no, p_vax, reduction_prob_h3 = run_h3(
        edges,
        num_days=120,
        num_runs=300,
        infection_prob=0.09,
        infectious_days=5,
        external_infection_prob=0.001,
        initial_infected=3,
        vaccination_coverage=0.30,
        large_outbreak_thresh=0.5,
    )

    #Plots
    plot_h1(mean_individual, mean_household)

    plot_h2(
        mean_peak_day_high,
        mean_peak_day_low,
        mean_peak_I_high,
        mean_peak_I_low,
    )

    plot_h3(p_no, p_vax)


if __name__ == "__main__":
    main()
