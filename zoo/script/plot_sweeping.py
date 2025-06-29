import sys
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
    base_dir = 'zoo/speedup'
    dir_cpu             = f'{base_dir}/bposd_surface_sweeping_cpu'
    dir_gpu_amd_mi210   = f'{base_dir}/bposd_surface_sweeping_gpu_amd_mi210'
    dir_gpu_nv_a100     = f'{base_dir}/bposd_surface_sweeping_gpu_nv_a100'
    dir_gpu_nv_h200     = f'{base_dir}/bposd_surface_sweeping_gpu_nv_h200'

    results_dict_cpu            = load_results_dict(dir_cpu)
    results_dict_gpu_amd_mi210  = load_results_dict(dir_gpu_amd_mi210)
    results_dict_gpu_nv_a100    = load_results_dict(dir_gpu_nv_a100)
    results_dict_gpu_nv_h200    = load_results_dict(dir_gpu_nv_h200)

    def plot_gpu_compare(ax, dtype='float64', metric='time'):
        # fix the physical error rate and compare different gpus
        tag_shared = [dtype, '11', 'hx', 'surface']
        tag_001 = tag_to_str(tag_shared + ['0.01'])
        tag_002 = tag_to_str(tag_shared + ['0.02'])
        tag_005 = tag_to_str(tag_shared + ['0.05'])
        tag_010 = tag_to_str(tag_shared + ['0.1'])
        tag_020 = tag_to_str(tag_shared + ['0.2'])
        tag_050 = tag_to_str(tag_shared + ['0.5'])

        if metric == 'time':
            full_decoding_metric = ['decoder_full', 'total time (s)']
        elif metric == 'accuracy':
            full_decoding_metric = ['decoder_full', 'logical error rate']

        result_tag_001_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_001])
        result_tag_001_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_001])
        result_tag_001_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_001])

        result_tag_002_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_002])
        result_tag_002_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_002])
        result_tag_002_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_002])

        result_tag_005_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_005])
        result_tag_005_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_005])
        result_tag_005_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_005])

        result_tag_010_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_010])
        result_tag_010_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_010])
        result_tag_010_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_010])

        result_tag_020_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_020])
        result_tag_020_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_020])
        result_tag_020_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_020])

        result_tag_050_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_050])
        result_tag_050_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_050])
        result_tag_050_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_050])

        # X-axis values
        x_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

        amd_mi210 = [
            result_tag_001_am2,
            result_tag_002_am2,
            result_tag_005_am2,
            result_tag_010_am2,
            result_tag_020_am2,
            result_tag_050_am2,
        ]

        nv_a100 = [
            result_tag_001_na1,
            result_tag_002_na1,
            result_tag_005_na1,
            result_tag_010_na1,
            result_tag_020_na1,
            result_tag_050_na1,
        ]

        nv_h200 = [
            result_tag_001_nh2,
            result_tag_002_nh2,
            result_tag_005_nh2,
            result_tag_010_nh2,
            result_tag_020_nh2,
            result_tag_050_nh2,
        ]
        
        colors = plt.get_cmap("tab10").colors[:3]
        markers = ['^', 'o', 's']

        color_labels = ['float64', 'float32', 'float16']
        marker_labels = ['AMD MI210', 'NVIDIA A100', 'NVIDIA H200']

        color_proxies = [Line2D([0], [0], color=c, lw=1) for c in colors]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=m, markerfacecolor='black', linestyle='none', markersize=4) for m in markers]

        # Combine labels
        legend_proxies = color_proxies + marker_proxies
        legend_labels = color_labels + marker_labels

        if dtype == 'float64':
            colors_here = colors[0]
        elif dtype == 'float32':
            colors_here = colors[1]
        elif dtype == 'float16':
            colors_here = colors[2]

        if dtype == 'float64':
            label_amd_mi210 = 'AMD MI210'
            label_nv_a100   = 'NVIDIA A100'
            label_nv_h200   = 'NVIDIA H200'
        else:
            label_amd_mi210 = None
            label_nv_a100   = None
            label_nv_h200   = None

        if dtype == 'float16':
            ax.legend(legend_proxies, legend_labels, 
                        handletextpad=0.1,  # Reduce space between marker and label
                        borderpad=0.25,      # Reduce space inside legend border
                        columnspacing=0.1,  # Reduce space between columns if multi-column
                        labelspacing=0.1,
                        handlelength=1)

        ax.plot(x_ticks, amd_mi210, marker=markers[0], label=label_amd_mi210, color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_a100, marker=markers[1], label=label_nv_a100, color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_h200, marker=markers[2], label=label_nv_h200, color=colors_here, markersize=4)

        # Axis labels and scale
        ax.set_xlabel("Physical error rate")
        if metric == 'time':
            ax.set_ylabel("Runtime (s)")
        elif metric == 'accuracy':
            ax.set_ylabel("Logical error rate")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x) for x in x_ticks])


    def plot_data_format_compare(ax, error_rate='0.02', metric='time'):
        # fig to compare different gpus
        tag_shared = [error_rate, '11', 'hx', 'surface']
        tag_16 = tag_to_str(tag_shared + ['float16'])
        tag_32 = tag_to_str(tag_shared + ['float32'])
        tag_64 = tag_to_str(tag_shared + ['float64'])

        if metric == 'time':
            full_decoding_metric = ['decoder_full', 'total time (s)']
        elif metric == 'accuracy':
            full_decoding_metric = ['decoder_full', 'logical error rate']

        result_tag_16_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_16])
        result_tag_16_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_16])
        result_tag_16_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_16])

        result_tag_32_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_32])
        result_tag_32_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_32])
        result_tag_32_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_32])

        result_tag_64_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_64])
        result_tag_64_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_64])
        result_tag_64_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_64])

        # X-axis values
        x_ticks = [16, 32, 64]

        amd_mi210 = [
            result_tag_16_am2,
            result_tag_32_am2,
            result_tag_64_am2,
        ]

        nv_a100 = [
            result_tag_16_na1,
            result_tag_32_na1,
            result_tag_64_na1,
        ]

        nv_h200 = [
            result_tag_16_nh2,
            result_tag_32_nh2,
            result_tag_64_nh2,
        ]

        colors = plt.get_cmap("tab10").colors[:3]
        markers = ['^', 'o', 's']

        color_labels = ['0.02', '0.05', '0.1']
        marker_labels = ['AMD MI210', 'NVIDIA A100', 'NVIDIA H200']

        color_proxies = [Line2D([0], [0], color=c, lw=1) for c in colors]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=m, markerfacecolor='black', linestyle='none', markersize=4) for m in markers]

        # Combine labels
        legend_proxies = color_proxies + marker_proxies
        legend_labels = color_labels + marker_labels

        if error_rate == '0.02':
            colors_here = colors[0]
        elif error_rate == '0.05':
            colors_here = colors[1]
        elif error_rate == '0.1':
            colors_here = colors[2]

        if error_rate == '0.02':
            label_amd_mi210 = 'AMD MI210'
            label_nv_a100   = 'NVIDIA A100'
            label_nv_h200   = 'NVIDIA H200'
        else:
            label_amd_mi210 = None
            label_nv_a100   = None
            label_nv_h200   = None

        if error_rate == '0.02':
            ax.legend(legend_proxies, legend_labels, 
                        handletextpad=0.1,  # Reduce space between marker and label
                        borderpad=0.25,      # Reduce space inside legend border
                        columnspacing=0.1,  # Reduce space between columns if multi-column
                        labelspacing=0.1,
                        handlelength=1)

        ax.plot(x_ticks, amd_mi210, marker=markers[0], label=label_amd_mi210, color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_a100, marker=markers[1], label=label_nv_a100, color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_h200, marker=markers[2], label=label_nv_h200, color=colors_here, markersize=4)

        # Axis labels and scale
        ax.set_xlabel("Data format")
        if metric == 'time':
            ax.set_ylabel("Runtime (s)")
        elif metric == 'accuracy':
            ax.set_ylabel("Logical error rate")
        # ax.set_xscale("log")
        # ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'float{str(x)}' for x in x_ticks])


    def plot_distance_compare(ax, distance='11', metric='time'):
        # fix gpu and data format and compare different distances
        tag_shared = [distance, 'float64', 'hx', 'surface']
        tag_001 = tag_to_str(tag_shared + ['0.01'])
        tag_002 = tag_to_str(tag_shared + ['0.02'])
        tag_005 = tag_to_str(tag_shared + ['0.05'])
        tag_010 = tag_to_str(tag_shared + ['0.1'])
        tag_020 = tag_to_str(tag_shared + ['0.2'])
        tag_050 = tag_to_str(tag_shared + ['0.5'])

        if metric == 'time':
            full_decoding_metric = ['decoder_full', 'total time (s)']
        elif metric == 'accuracy':
            full_decoding_metric = ['decoder_full', 'logical error rate']

        result_tag_001_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_001])
        result_tag_001_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_001])
        result_tag_001_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_001])

        result_tag_002_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_002])
        result_tag_002_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_002])
        result_tag_002_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_002])

        result_tag_005_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_005])
        result_tag_005_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_005])
        result_tag_005_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_005])

        result_tag_010_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_010])
        result_tag_010_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_010])
        result_tag_010_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_010])

        result_tag_020_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_020])
        result_tag_020_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_020])
        result_tag_020_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_020])

        result_tag_050_am2 = lookup_results_dict(results_dict_gpu_amd_mi210,   full_decoding_metric + [tag_050])
        result_tag_050_na1 = lookup_results_dict(results_dict_gpu_nv_a100,     full_decoding_metric + [tag_050])
        result_tag_050_nh2 = lookup_results_dict(results_dict_gpu_nv_h200,     full_decoding_metric + [tag_050])

        # X-axis values
        x_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

        amd_mi210 = [
            result_tag_001_am2,
            result_tag_002_am2,
            result_tag_005_am2,
            result_tag_010_am2,
            result_tag_020_am2,
            result_tag_050_am2,
        ]

        nv_a100 = [
            result_tag_001_na1,
            result_tag_002_na1,
            result_tag_005_na1,
            result_tag_010_na1,
            result_tag_020_na1,
            result_tag_050_na1,
        ]

        nv_h200 = [
            result_tag_001_nh2,
            result_tag_002_nh2,
            result_tag_005_nh2,
            result_tag_010_nh2,
            result_tag_020_nh2,
            result_tag_050_nh2,
        ]
        
        colors = plt.get_cmap("tab10").colors[:3]
        markers = ['^', 'o', 's']

        color_labels = ['3', '7', '11']
        marker_labels = ['AMD MI210', 'NVIDIA A100', 'NVIDIA H200']

        color_proxies = [Line2D([0], [0], color=c, lw=1) for c in colors]
        marker_proxies = [Line2D([0], [0], color='black', lw=0, marker=m, markerfacecolor='black', linestyle='none', markersize=4) for m in markers]

        # Combine labels
        legend_proxies = color_proxies + marker_proxies
        legend_labels = color_labels + marker_labels

        if distance == '3':
            colors_here = colors[0]
        elif distance == '7':
            colors_here = colors[1]
        elif distance == '11':
            colors_here = colors[2]

        if distance == '3':
            ax.legend(legend_proxies, legend_labels, 
                        handletextpad=0.1,  # Reduce space between marker and label
                        borderpad=0.25,      # Reduce space inside legend border
                        columnspacing=0.1,  # Reduce space between columns if multi-column
                        labelspacing=0.1,
                        handlelength=1)

        ax.plot(x_ticks, amd_mi210, marker=markers[0], color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_a100, marker=markers[1], color=colors_here, markersize=4)
        ax.plot(x_ticks, nv_h200, marker=markers[2], color=colors_here, markersize=4)

        # Axis labels and scale
        ax.set_xlabel("Physical error rate")
        if metric == 'time':
            ax.set_ylabel("Runtime (s)")
        elif metric == 'accuracy':
            ax.set_ylabel("Logical error rate")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x) for x in x_ticks])


    # Plot gpu
    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'time'
    plot_gpu_compare(ax, 'float64', metric)
    plot_gpu_compare(ax, 'float32', metric)
    plot_gpu_compare(ax, 'float16', metric)
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_gpu.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'accuracy'
    plot_gpu_compare(ax, 'float64', metric)
    plot_gpu_compare(ax, 'float32', metric)
    plot_gpu_compare(ax, 'float16', metric)
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_gpu.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)

    
    
    # Plot data format
    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'time'
    plot_data_format_compare(ax, '0.02', 'time')
    plot_data_format_compare(ax, '0.05', 'time')
    plot_data_format_compare(ax, '0.1', 'time')
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_data_format.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'accuracy'
    plot_data_format_compare(ax, '0.02', 'accuracy')
    plot_data_format_compare(ax, '0.05', 'accuracy')
    plot_data_format_compare(ax, '0.1', 'accuracy')
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_data_format.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)



    # Plot distance
    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'time'
    plot_distance_compare(ax, '3', 'time')
    plot_distance_compare(ax, '7', 'time')
    plot_distance_compare(ax, '11', 'time')
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_distance.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(3.33, 2.5))
    metric = 'accuracy'
    plot_distance_compare(ax, '3', 'accuracy')
    plot_distance_compare(ax, '7', 'accuracy')
    plot_distance_compare(ax, '11', 'accuracy')
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(f"{base_dir}/{metric}_distance.pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    main()

