from src.data_processing import load_malawi_contacts, split_into_days, daily_edge_lists
from src.analysis_h1 import run_h1
from src.analysis_h2 import run_h2
from src.analysis_h3 import run_h3

def main():
    df = load_malawi_contacts("data/malawi_contacts.csv")
    days = split_into_days(df)
    edges = daily_edge_lists(days)

    # ===== DEBUG BLOCK =====
    for d, e in edges.items():
        print("Day", d, "edges:", len(e))
        break
    # =======================
    
    reduction_h1 = run_h1(edges)
    delay_h2, reduction_peak_h2 = run_h2(edges)
    p_no, p_vax, reduction_prob_h3 = run_h3(edges)

    # Optionally print a summary or save results

if __name__ == "__main__":
    main()
