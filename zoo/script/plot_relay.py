import sys, shutil
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.lines import Line2D

# Get the directory containing the current Python file
current_path = Path(__file__).resolve().parent.parent.parent

# Add to sys.path (if not already there)
if str(current_path) not in sys.path:
    sys.path.insert(0, str(current_path))

from zoo.script.plot_utils import load_results_dict, tag_to_str, is_substring, lookup_results_dict

def main():
    base_dir = "zoo/relay_results"

    dir_bp_relay = f'{base_dir}/bp_relay_sweeping'
    dir_bposd = f'{base_dir}/bposd_sweeping'

    results_relay = load_results_dict(dir_bp_relay)
    results_bposd = load_results_dict(dir_bposd)

    def plot_data_format_compare(ax, error_rate='0.02', metric='time'):
        # fig to compare different gpus
        tag_shared = [error_rate, '11', 'hx', 'surface']
        tags = []

        if metric == 'time':
            full_decoding_metric = ['decoder_full', 'total time (s)']
        elif metric == 'accuracy':
            full_decoding_metric = ['decoder_full', 'logical error rate']

        # X-axis values
        x_ticks = [16, 32, 64]

        for err in x_ticks:
            tags.append(tag_to_str(tag_shared + [f'float{err}']))
        
        bp_relay_tags = []
        for tag in tags:
            bp_relay_tags.append(lookup_results_dict(results_relay,   full_decoding_metric + [tag]))
        
        bposd_tags = []
        for tag in tags:
            bposd_tags.append(lookup_results_dict(results_bposd,    full_decoding_metric + [tag]))
        
        colors = plt.get_cmap("tab10").colors[:3]
        markers = ['^', 'o', 's']

        color_labels = ['0.01', '0.05', '0.1']
        marker_labels = ['bp_relay', 'bposd']

        color_proxies = [Line2D([0], [0], color=c, lw=1) for c in colors]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=m, markerfacecolor='black', linestyle='none', markersize=4) for m in markers]

        # Combine labels
        legend_proxies = color_proxies + marker_proxies
        legend_labels = color_labels + marker_labels

        if error_rate == '0.01':
            colors_here = colors[0]
        elif error_rate == '0.05':
            colors_here = colors[1]
        elif error_rate == '0.1':
            colors_here = colors[2]

        if error_rate == '0.01':
            label_relay = 'bp_relay'
            label_bposd = 'bposd'
        else:
            label_relay = None
            label_bposd = None

        if error_rate == '0.02':
            ax.legend(legend_proxies, legend_labels, 
                        loc='best',
                        ncol=3,
                        handletextpad=0.1,  # Reduce space between marker and label
                        borderpad=0.25,      # Reduce space inside legend border
                        columnspacing=0.1,  # Reduce space between columns if multi-column
                        labelspacing=0.1,
                        handlelength=1)

        ax.plot(x_ticks, bp_relay_tags, marker=markers[0], label=label_relay, color=colors_here, markersize=4)
        ax.plot(x_ticks, bposd_tags, marker=markers[1], label=label_bposd, color=colors_here, markersize=4)


        # Axis labels and scale
        ax.set_xlabel("Data format")
        if metric == 'time':
            ax.set_ylabel("Runtime (s)")
        elif metric == 'accuracy':
            ax.set_ylabel("Logical error rate")
        # ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'FP{str(x)}' for x in x_ticks])

    FIGWIDHT = 3.33
    FIGHEIGHT = 2

    # PLOT #
    fig, ax = plt.subplots(figsize=(FIGWIDHT, FIGHEIGHT))
    metric = 'time'
    plot_data_format_compare(ax, '0.01', metric)
    plot_data_format_compare(ax, '0.05', metric)
    plot_data_format_compare(ax, '0.1', metric)
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_data_format.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/{metric}_data_format.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(FIGWIDHT, FIGHEIGHT))
    metric = 'accuracy'
    plot_data_format_compare(ax, '0.01', metric)
    plot_data_format_compare(ax, '0.05', metric)
    plot_data_format_compare(ax, '0.1', metric)
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_data_format.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{base_dir}/{metric}_data_format.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

if __name__ == '__main__':
    main()