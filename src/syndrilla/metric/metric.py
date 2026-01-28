import torch, time, os
import yaml
import numpy as np

from loguru import logger


def report_metric(num_max_iter, e_estimated, e_actual, iteration, time_iteration, check, converge, converge_next, decode_idx):
    """
    This function reports the decoding iteration and accuracy.
    """
    
    logger.info(f'Reporting decoding metric for decoder {decode_idx}.')
    
    sample_size = e_estimated.shape[0]
    number_channel = e_actual.shape[1]
    dtype = e_estimated.dtype
    total_time = np.sum(time_iteration)
    logger.info(f'Total time for <{sample_size}> samples: {total_time} seconds.')

    if iteration.numel() == 0:
        average_iter = 0.0
        distribution = torch.zeros(num_max_iter+1).to(e_estimated.device)
    else:
        distribution = torch.bincount((iteration - 1).int(), minlength=num_max_iter+1).int().to(e_estimated.device)
        average_iter = torch.mean(iteration).item()

    logger.info(f'Average iterations per sample: {average_iter}')
    logger.info(f'Maximum iterations: {distribution}')

    if total_time == 0:
        average_time_sample = 0
        logger.info(f'Average time per sample: {average_time_sample} seconds.')
        
        average_time_sample_iter = 0
        logger.info(f'Average time per iteration: {average_time_sample_iter}')
    else:
        average_time_sample = total_time/sample_size
        logger.info(f'Average time per sample: {average_time_sample} seconds.')
        
        average_time_sample_iter = (average_time_sample/average_iter).item()
        logger.info(f'Average time per iteration: {average_time_sample_iter}')

    if torch.isinf(torch.sum(converge)) or torch.isnan(torch.sum(converge)):
        invoke_rate = 1.0
        logger.info(f'Decoder invoke rate: {invoke_rate}')
    else:
        if int(torch.sum(converge)) == 0:
            invoke_rate = 1.0
            logger.info(f'Decoder invoke rate: {invoke_rate}')
        else:
            invoke_rate = 1.0 - ((int(torch.sum(converge)))/sample_size)
            logger.info(f'Decoder invoke rate: {invoke_rate}')

    # e_estimated = e_estimated.to(e_estimated.device)
    if e_actual.size(1) <= 1:
        e_estimated = e_estimated.unsqueeze(1).expand(-1, e_actual.size(1), -1)
    data_qubit_acc = torch.zeros([number_channel], dtype=dtype)
    correction_acc = torch.zeros([number_channel], dtype=dtype)
    data_frame_error_rate = torch.zeros([number_channel], dtype=dtype)
    synd_frame_error_rate = torch.zeros([number_channel], dtype=dtype)
    logical_error_rate = torch.zeros([number_channel], dtype=dtype)
    converge_succ_rate = torch.zeros([number_channel], dtype=dtype)
    converge_fail_rate = torch.zeros([number_channel], dtype=dtype)
    for i in range(e_actual.size(1)):  # iterate over check_type
        check_channel = check[:, i] 
        e_actual_channel = e_actual[:, i, :]
        e_estimated_channel = e_estimated[:, i, :]
        eq_i = (e_estimated_channel == e_actual_channel)
        comp_i = torch.unique(eq_i, return_counts=True)[1]
        if int(comp_i.shape[0]) == 1:
            data_qubit_acc[i] = 1.0
        else:
            data_qubit_acc[i] = float(comp_i[1]) / (float(comp_i[1]) + float(comp_i[0]))

        num_error = torch.sum(e_estimated_channel != e_actual_channel)
    
        total_ones = torch.sum((e_estimated_channel == 1) | (e_actual_channel == 1))
        if float(num_error) == 0:
            correction_acc[i] = 1
        else:
            correction_acc[i] = (1 - float(num_error)/float(total_ones))

        result = (e_estimated_channel == e_actual_channel).all(dim=1).int()
        num_correct = (result == 1).sum()
        num_incorrect = (result == 0).sum()
        if int(result.shape[0]) == 1:
            data_frame_error_rate[i] = 0.0
        else:
            data_frame_error_rate[i] = float(num_incorrect) / (float(num_incorrect) + float(num_correct))
            
        if torch.isinf(torch.sum(converge_next)) or torch.isnan(torch.sum(converge_next)):
            synd_frame_error_rate[i] = 0
        else:
            if int(torch.sum(converge_next)) == 0:
                synd_frame_error_rate[i] = 0.0
            else:
                synd_frame_error_rate[i] = ((check_channel.size()[0] - int(torch.sum(converge_next)))/(check_channel.size()[0]))
        
        if int(torch.sum(check_channel)) == 0:
            logical_error_rate[i] = 0
        else:
            logical_error_rate[i] = (int(torch.sum(check_channel))/(check_channel.size()[0]))
        
        converge_fail = torch.where((check_channel == 1) & (converge_next == 1), torch.tensor(1), torch.tensor(0))
        if int(torch.sum(converge_fail)) == 0:
            converge_fail_rate[i] = 0
        else:
            converge_fail_rate[i] = (int(torch.sum(converge_fail))/(check.size()[0]))
        
        converge_succ = torch.where((check_channel == 0) & (converge_next == 1), torch.tensor(1), torch.tensor(0))
        if int(torch.sum(converge_succ)) == 0:
            converge_succ_rate[i] = 0
        else:
            converge_succ_rate[i] = (int(torch.sum(converge_succ))/(check_channel.size()[0]))

        for channel in range(number_channel):
            logger.info(f'Channel {channel} metrics:')
            logger.info(f'  Data qubit accuracy: {data_qubit_acc[channel]:.6f}')
            logger.info(f'  Correction accuracy: {correction_acc[channel]:.6f}')
            logger.info(f'  Data frame error rate: {data_frame_error_rate[channel]:.6f}')
            logger.info(f'  Syndrome frame error rate: {synd_frame_error_rate[channel]:.6f}')
            logger.info(f'  Logical error rate: {logical_error_rate[channel]:.6f}')
            logger.info(f'  Converge failure rate: {converge_fail_rate[channel]:.6f}')
            logger.info(f'  Converge success rate: {converge_succ_rate[channel]:.6f}')

    return total_time, average_time_sample, average_iter, distribution, average_time_sample_iter, \
        data_qubit_acc, data_frame_error_rate, synd_frame_error_rate, \
            correction_acc, logical_error_rate, invoke_rate, converge_fail_rate, converge_succ_rate


def save_metric(out_dict, curr_dir, batch_size, target_error, dtype, physical_error_rate, num_batches, error_reach, file_name, check_num, done=0):
    """
    Saves decoding metrics for all decoders into a single YAML file.
    
    Parameters:
        out_dict (list of dicts): each item is a dict with metric keys
        curr_dir (str): directory path to save YAML
        physical_error_rate (float or str): label for file naming
    """

    logger.info('Saving all decoding metrics to a YAML file.')
    
    def float_representer(dumper, value):
        return dumper.represent_scalar('tag:yaml.org,2002:float', f"{value:.17e}")
    
    def list_representer(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
    
    def format_time(value):
        return f'{float(value):.17e}'
    
    all_metrics_results = {}
    total_time_sum = 0.0
    all_check_types = ['hx', 'hz']
    final_list = []
    
    for i, decoder_metrics in enumerate(out_dict):
        decoder_key = f'decoder_{i}'
        if done:
            total = decoder_metrics['distribution'].sum()
            cdf = torch.cumsum(decoder_metrics['distribution'], dim=0) / total
            qs = torch.linspace(0.0, 1.0, 101, device=decoder_metrics['distribution'].device)
            indices = torch.searchsorted(cdf, qs, right=False)
            distribution = (indices + 1).int().tolist()
        else:
            distribution = decoder_metrics['distribution'].int().cpu().numpy().tolist()
        
        total_time_sum += float(decoder_metrics['total_time'])
        data_acc = decoder_metrics['data_qubit_acc']
        if not isinstance(data_acc, (list, tuple)):
            data_acc = [data_acc]
        
        check_list = []
        for idx in range(len(data_acc)):
            check_list.append({
                'data qubit accuracy': float(decoder_metrics['data_qubit_acc'][idx] if isinstance(decoder_metrics['data_qubit_acc'], (list, tuple)) else decoder_metrics['data_qubit_acc']),
                'data qubit correction accuracy': float(decoder_metrics['correction_acc'][idx] if isinstance(decoder_metrics['correction_acc'], (list, tuple)) else decoder_metrics['correction_acc']),
                'data frame error rate': float(decoder_metrics['data_frame_error_rate'][idx] if isinstance(decoder_metrics['data_frame_error_rate'], (list, tuple)) else decoder_metrics['data_frame_error_rate']),
                'syndrome frame error rate': float(decoder_metrics['synd_frame_error_rate'][idx] if isinstance(decoder_metrics['synd_frame_error_rate'], (list, tuple)) else decoder_metrics['synd_frame_error_rate']),
                'logical error rate': float(decoder_metrics['logical_error_rate'][idx] if isinstance(decoder_metrics['logical_error_rate'], (list, tuple)) else decoder_metrics['logical_error_rate']),
                'converge failure rate': float(decoder_metrics['converge_fail_rate'][idx] if isinstance(decoder_metrics['converge_fail_rate'], (list, tuple)) else decoder_metrics['converge_fail_rate']),
                'converge success rate': float(decoder_metrics['converge_succ_rate'][idx] if isinstance(decoder_metrics['converge_succ_rate'], (list, tuple)) else decoder_metrics['converge_succ_rate']),
            })
            final_list.append({
                'logical error rate': float(decoder_metrics['logical_error_rate'][idx] if isinstance(decoder_metrics['logical_error_rate'], (list, tuple)) else decoder_metrics['logical_error_rate'])
            })
        
        check_types = [all_check_types[check_num]] if len(check_list) == 1 else ['hx', 'hz']
        all_metrics_results[decoder_key] = {
            'algorithm': decoder_metrics['algorithm'],
            'decoder invoke rate': float(decoder_metrics['invoke_rate']),
            'average iteration': float(decoder_metrics['average_iter']),
            'distribution': distribution,
            'total time (s)': format_time(decoder_metrics['total_time']),
            'average time per batch (s)': format_time(decoder_metrics['total_time']/num_batches),
            'average time per sample (s)': format_time(decoder_metrics['average_time_sample']),
            'average time per iteration (s)': format_time(decoder_metrics['average_time_sample_iter']),
        }
        for idx, check_name in enumerate(check_types[:len(check_list)]):
            all_metrics_results[decoder_key][f'{check_name}'] = check_list[idx]
    
    all_metrics_results['decoder_full'] = {
        'batch size': batch_size,
        'batch count': num_batches,
        'target error': target_error,
        'target error reached': error_reach,
        'data type': dtype,
        'physical error rate': physical_error_rate,
        'total time (s)': format_time(total_time_sum),
        'H matrix': file_name,
    }
    for idx, check_name in enumerate(check_types[:len(final_list)]):
        all_metrics_results['decoder_full'][f'{check_name}'] = final_list[idx]
    
    os.makedirs(curr_dir, exist_ok=True)
    output_path = os.path.join(curr_dir, f'result_phy_err_{physical_error_rate}.yaml')
    
    # Add custom representers for proper formatting
    yaml.SafeDumper.add_representer(float, float_representer)
    yaml.SafeDumper.add_representer(list, list_representer)
    
    with open(output_path, 'w') as f:
        yaml.safe_dump(all_metrics_results, f, sort_keys=False, default_flow_style=False)


def compute_avg_metrics(target_error, i, num_batches,
                        total_time_all,
                        average_time_sample_all,
                        average_iter_all,
                        distribution_all,
                        average_time_sample_iter_all,
                        data_qubit_acc,
                        data_frame_error_rate_all,
                        synd_frame_error_rate_all,
                        correction_acc_all,
                        logical_error_rate_all,
                        invoke_rate_all,
                        converge_fail_all,
                        converge_succ_all):
    logger.info(f'Reporting decoding metric for decoder {i}.')
    total_time = total_time_all[i]
    average_time_batch = total_time / num_batches
    average_time_sample = average_time_sample_all[i] / num_batches
    average_iter = average_iter_all[i] / num_batches
    distribution = distribution_all[i]
    average_time_sample_iter = average_time_sample_iter_all[i] / num_batches
    invoke_rate = invoke_rate_all[i] / num_batches
    logger.info(f'Decoder invoke rate: {invoke_rate}')

    logger.info(f'Total time for <{target_error}> errors: {total_time} seconds.')
    logger.info(f'Total number of batches: {num_batches}.')
    logger.info(f'Average time per batch: {average_time_batch} seconds.')
    logger.info(f'Average time per sample: {average_time_sample} seconds.')
    logger.info(f'Average iterations per sample: {average_iter}')
    logger.info(f'Distribution: {distribution}')
    logger.info(f'Average time per iteration: {average_time_sample_iter}')
    
    average_data_qubit_acc =  [x / num_batches for x in data_qubit_acc[i]]
    average_correction_acc = [x / num_batches for x in correction_acc_all[i]]
    average_data_frame_error_rate = [x / num_batches for x in data_frame_error_rate_all[i]]
    average_synd_frame_error_rate = [x / num_batches for x in synd_frame_error_rate_all[i]]
    average_logical_error_rate = [x / num_batches for x in logical_error_rate_all[i]]
    average_converge_fail = [x / num_batches for x in converge_fail_all[i]]
    average_converge_succ = [x / num_batches for x in converge_succ_all[i]]

    number_channel = len(data_qubit_acc[i])
    for channel in range(number_channel):
        logger.info(f'Channel idx: {channel}')
        logger.info(f'Data qubit accuracy: {average_data_qubit_acc[channel]}')
        logger.info(f'Data qubit correction accuracy: {average_correction_acc[channel]}')
        logger.info(f'Data frame error rate: {average_data_frame_error_rate[channel]}')
        logger.info(f'Syndrome frame error rate: {average_synd_frame_error_rate[channel]}')
        logger.info(f'Output logical error rate: {average_logical_error_rate[channel]}')
        logger.info(f'converge failure rate: {average_converge_fail[channel]}')
        logger.info(f'Converge success rate: {average_converge_succ[channel]}')
    logger.info(f'Complete.')

    return total_time, average_time_sample, average_iter, distribution, average_time_sample_iter, average_data_qubit_acc, \
        average_data_frame_error_rate, average_synd_frame_error_rate, average_correction_acc, average_logical_error_rate, \
            invoke_rate, average_converge_fail, average_converge_succ


def load_checkpoint_yaml(path, number_channel):
     with open(path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")
        
        full = data['decoder_full']
        ckpt_H = full.get('H matrix', 0)
        batch_size = int(full.get('batch size', 0))
        batch_count = int(full.get('batch count', 0))
        target_error = int(full.get('target error', 0))
        error_reach = int(full.get('target error reached', 0))
        dtype = full.get('data type', 0)
        physical_error_rate = float(full.get('physical error rate', 0.0))
    
        decoder_keys = sorted(
            [k for k in data if k.startswith('decoder_') and k[8:].isdigit()],
            key=lambda x: int(x.split('_')[1])
        )
        num_decoders = len(decoder_keys)

        # Initialize lists
        total_time_all              = [0.0 for _ in range(num_decoders)]
        average_time_sample_all     = [0.0 for _ in range(num_decoders)]
        average_iter_all            = [0.0 for _ in range(num_decoders)]
        distribution_all            = [0.0 for _ in range(num_decoders)]
        average_time_sample_iter_all= [0.0 for _ in range(num_decoders)]
        invoke_rate_all             = [0.0 for _ in range(num_decoders)]
        data_qubit_acc_all          = [([0.0] * number_channel) for _ in range(num_decoders)]
        data_frame_error_rate_all   = [([0.0] * number_channel) for _ in range(num_decoders)]
        synd_frame_error_rate_all   = [([0.0] * number_channel) for _ in range(num_decoders)]
        correction_acc_all          = [([0.0] * number_channel) for _ in range(num_decoders)]
        logical_error_rate_all      = [([0.0] * number_channel) for _ in range(num_decoders)]
        converge_fail_all           = [([0.0] * number_channel) for _ in range(num_decoders)]
        converge_succ_all           = [([0.0] * number_channel) for _ in range(num_decoders)]

        # Populate from YAML
        for idx, key in enumerate(decoder_keys):
            entry = data[key]

            has_hx = 'hx' in entry
            has_hz = 'hz' in entry

            if has_hx and has_hz:
                ch_map = [('hx', 0), ('hz', 1)]
            else:
                if has_hx:
                    ch_map = [('hx', 0)]
                elif has_hz:
                    ch_map = [('hz', 0)]
                else:
                    ch_map = []
            total_time_all[idx] = float(entry['total time (s)'])*batch_count
            average_time_sample_all[idx] = float(entry['average time per sample (s)'])*batch_count
            average_iter_all[idx] = float(entry['average iteration'])*batch_count
            distribution_all[idx] = torch.tensor(entry['distribution'])
            average_time_sample_iter_all[idx] = float(entry['average time per iteration (s)'])*batch_count
            invoke_rate_all[idx] = float(entry['decoder invoke rate'])*batch_count

            for ch, ch_idx in ch_map:
                ch_entry = entry[ch]

                data_qubit_acc_all[idx][ch_idx] = float(ch_entry.get('data qubit accuracy', 0.0)) * batch_count
                data_frame_error_rate_all[idx][ch_idx] = float(ch_entry.get('data frame error rate', 0.0)) * batch_count
                synd_frame_error_rate_all[idx][ch_idx] = float(ch_entry.get('syndrome frame error rate', 0.0)) * batch_count
                correction_acc_all[idx][ch_idx] = float(ch_entry.get('data qubit correction accuracy', 0.0)) * batch_count
                logical_error_rate_all[idx][ch_idx] = float(ch_entry.get('logical error rate', 0.0)) * batch_count
                converge_fail_all[idx][ch_idx] = float(ch_entry.get('converge failure rate', 0.0)) * batch_count
                converge_succ_all[idx][ch_idx] = float(ch_entry.get('converge success rate', 0.0)) * batch_count

        return (total_time_all,
                average_time_sample_all,
                average_iter_all,
                distribution_all,
                average_time_sample_iter_all,
                data_qubit_acc_all,
                data_frame_error_rate_all,
                synd_frame_error_rate_all,
                correction_acc_all,
                logical_error_rate_all,
                invoke_rate_all,
                converge_fail_all,
                converge_succ_all, error_reach, batch_size, target_error, dtype, physical_error_rate, batch_count, ckpt_H)
     
