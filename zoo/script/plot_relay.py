import sys, shutil
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.lines import Line2D

# Get the directory containing the current Python file
current_path = Path(__file__).resolve().parent.parent.parent

# Add to sys.path (if not already there)
if str(current_path) not in sys.path:
    sys.path.insert(0, str(current_path))

from zoo.script.plot_utils import load_results_dict, tag_to_str, is_substring, lookup_results_dict

def main():
    base_dir = "zoo/"

    dir_bp_relay = f'{base_dir}/bp_relay_sweeping'
    dir_bposd = f'{base_dir}/bposd_sweeping'

    results_relay = load_results_dict(dir_bp_relay)
    results_bposd = load_results_dict(dir_bposd)

    FIGWIDTH = 3.33
    FIGHEIGHT = 2

    dtype = 'float32'
    code = 'hx'
    code_family = 'surface'

    decoder_results = {
        'bp_relay': results_relay,
        'bposd':    results_bposd,
    }
    colors  = {'bp_relay': 'tab:blue', 'bposd': 'tab:orange'}
    markers = {'bp_relay': '^',        'bposd': 'o'}

    # x-offset multiplier for log and linear scales
    log_offsets   = {'bp_relay': 0.92, 'bposd': 1.08}
    lin_offsets   = {'bp_relay': -0.15, 'bposd': 0.15}

    # ------------------------------------------------------------------ #
    # PLOT 1: Logical error rate vs distance for fixed physical error rates
    # ------------------------------------------------------------------ #
    def plot_logical_vs_distance(ax):
        distances = ['3', '7', '11']
        distance_vals = [3, 7, 11]
        fixed_error_rates = [0.02, 0.05, 0.1]

        rate_colors = {
            0.02: plt.get_cmap("tab10").colors[0],
            0.05: plt.get_cmap("tab10").colors[1],
            0.1:  plt.get_cmap("tab10").colors[2],
        }

        for p in fixed_error_rates:
            for decoder, results in decoder_results.items():
                x_vals = []
                y_vals = []
                for d, dval in zip(distances, distance_vals):
                    tag = tag_to_str([str(p), d, dtype, code, code_family])
                    val = lookup_results_dict(results, [tag, 'decoder_full', 'logical error rate'])
                    if val is not None and val > 0:
                        x_vals.append(dval + lin_offsets[decoder])
                        y_vals.append(val)
                if x_vals:
                    ax.plot(x_vals, y_vals,
                            marker=markers[decoder],
                            color=rate_colors[p],
                            markersize=4,
                            linestyle='--' if decoder == 'bposd' else '-')

        rate_proxies = [Line2D([0], [0], color=rate_colors[p], lw=1) for p in fixed_error_rates]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=markers[dec],
                                 markerfacecolor='black', linestyle='none', markersize=4)
                          for dec in decoder_results]
        ax.legend(rate_proxies + marker_proxies,
                  [str(p) for p in fixed_error_rates] + list(decoder_results.keys()),
                  fontsize='x-small', framealpha=1.0, loc='best', ncol=2,
                  handletextpad=0.1, borderpad=0.25, columnspacing=0.1,
                  labelspacing=0.1, handlelength=1)

        ax.set_xlabel("Distance")
        ax.set_ylabel("Logical error rate")
        ax.set_yscale("log")
        ax.set_xticks(distance_vals)
        ax.set_xticklabels([str(d) for d in distance_vals])
        ax.grid(True)

    # ------------------------------------------------------------------ #
    # PLOT 2: Average iterations vs distance
    # ------------------------------------------------------------------ #
    def plot_avg_iterations_vs_distance(ax):
        distances = ['3', '7', '11']
        distance_vals = [3, 7, 11]
        fixed_error_rates = [0.02, 0.05, 0.1]

        rate_colors = {
            0.02: plt.get_cmap("tab10").colors[0],
            0.05: plt.get_cmap("tab10").colors[1],
            0.1:  plt.get_cmap("tab10").colors[2],
        }

        for p in fixed_error_rates:
            for decoder, results in decoder_results.items():
                x_vals = []
                y_vals = []
                for d, dval in zip(distances, distance_vals):
                    tag = tag_to_str([str(p), d, dtype, code, code_family])
                    val = lookup_results_dict(results, [tag, 'decoder_0', 'average iteration'])
                    if val is not None and val > 0:
                        x_vals.append(dval + lin_offsets[decoder])
                        y_vals.append(val)
                if x_vals:
                    ax.plot(x_vals, y_vals,
                            marker=markers[decoder],
                            color=rate_colors[p],
                            markersize=4,
                            linestyle='--' if decoder == 'bposd' else '-')

        rate_proxies = [Line2D([0], [0], color=rate_colors[p], lw=1) for p in fixed_error_rates]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=markers[dec],
                                 markerfacecolor='black', linestyle='none', markersize=4)
                          for dec in decoder_results]
        ax.legend(rate_proxies + marker_proxies,
                  [str(p) for p in fixed_error_rates] + list(decoder_results.keys()),
                  fontsize='x-small', framealpha=1.0, loc='best', ncol=2,
                  handletextpad=0.1, borderpad=0.25, columnspacing=0.1,
                  labelspacing=0.1, handlelength=1)

        ax.set_xlabel("Distance")
        ax.set_ylabel("Average iterations")
        ax.set_xticks(distance_vals)
        ax.set_xticklabels([str(d) for d in distance_vals])
        ax.grid(True)

    # ------------------------------------------------------------------ #
    # PLOT 3: Average time per sample vs physical error rate
    # ------------------------------------------------------------------ #
    def plot_time_per_sample_vs_phys(ax):
        distance = '11'
        x_ticks = [0.02, 0.05, 0.1, 0.2, 0.5]

        for decoder, results in decoder_results.items():
            x_vals = []
            y_vals = []
            for p in x_ticks:
                tag = tag_to_str([str(p), distance, dtype, code, code_family])
                val = lookup_results_dict(results, [tag, 'decoder_0', 'average time per sample (s)'])
                if val is not None and val > 0:
                    x_vals.append(p * log_offsets[decoder])
                    y_vals.append(val)
            if x_vals:
                ax.plot(x_vals, y_vals,
                        marker=markers[decoder],
                        color=colors[decoder],
                        label=decoder,
                        markersize=4,
                        linestyle='--' if decoder == 'bposd' else '-')

        ax.set_xlabel("Physical error rate")
        ax.set_ylabel("Avg time per sample (s)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x) for x in x_ticks])
        ax.legend(fontsize='x-small', framealpha=1.0, loc='best')
        ax.grid(True)

    # ------------------------------------------------------------------ #
    # PLOT 4: Logical vs physical error rate
    # ------------------------------------------------------------------ #
    def plot_phys_vs_logical_relay_vs_bposd(ax):
        distance = '11'
        x_ticks = [0.02, 0.05, 0.1, 0.2, 0.5]

        for decoder, results in decoder_results.items():
            x_vals, y_vals = [], []
            for p in x_ticks:
                tag = tag_to_str([str(p), distance, dtype, code, code_family])
                val = lookup_results_dict(results, [tag, 'decoder_full', 'logical error rate'])
                if val is not None and val > 0:
                    x_vals.append(p * log_offsets[decoder])
                    y_vals.append(val)
            if x_vals:
                ax.plot(x_vals, y_vals,
                        marker=markers[decoder],
                        color=colors[decoder],
                        label=decoder,
                        markersize=4,
                        linestyle='--' if decoder == 'bposd' else '-')

        ax.set_xlabel("Physical error rate")
        ax.set_ylabel("Logical error rate")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x) for x in x_ticks])
        ax.legend(fontsize='x-small', framealpha=1.0, loc='best')
        ax.grid(True)

    # --- Save all plots --- #

    fig, ax = plt.subplots(figsize=(FIGWIDTH, FIGHEIGHT))
    plot_phys_vs_logical_relay_vs_bposd(ax)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/logical_vs_physical_d11_hx.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/logical_vs_physical_d11_hx.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(FIGWIDTH, FIGHEIGHT))
    plot_logical_vs_distance(ax)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/logical_vs_distance_hx.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/logical_vs_distance_hx.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(FIGWIDTH, FIGHEIGHT))
    plot_avg_iterations_vs_distance(ax)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/avg_iterations_vs_distance_hx.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/avg_iterations_vs_distance_hx.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(FIGWIDTH, FIGHEIGHT))
    plot_time_per_sample_vs_phys(ax)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/time_per_sample_vs_physical_d11_hx.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/time_per_sample_vs_physical_d11_hx.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

if __name__ == '__main__':
    main()