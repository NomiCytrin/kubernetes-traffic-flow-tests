#!/usr/bin/env python3
"""
Simple parser for Kubernetes Traffic Flow Test results to CSV.
"""

import json
import argparse
import pandas as pd
from pathlib import Path


def parse_test_file(file_path: str) -> list:
    """Parse a test file and return list of test data for CSV."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    results = []
    
    for test in data.get('tft-tests', []):
        flow_test = test.get('flow_test', {})
        metadata = flow_test.get('tft_metadata', {})
        
        # Extract basic test info
        test_case = metadata.get('test_case_id', 'Unknown')
        test_type = metadata.get('test_type', 'Unknown')
        reverse = metadata.get('reverse', False)
        success = flow_test.get('success', False)
        error_msg = flow_test.get('msg', '') if not success else ''
                
        # Extract server and client names
        server_info = metadata.get('server', {})
        client_info = metadata.get('client', {})
        server_name = server_info.get('name', 'Unknown')
        client_name = client_info.get('name', 'Unknown')
        
        # Extract bitrates
        bitrate_data = flow_test.get('bitrate_gbps', {})
        tx_bitrate = bitrate_data.get('tx') if bitrate_data else None
        rx_bitrate = bitrate_data.get('rx') if bitrate_data else None
        
        # Extract plugin success status and detailed information
        plugin_success = {}
        plugin_details = {}
        bandwidth_threshold = None
        bandwidth_validation_msg = ''
        plugin_failure_messages = []
        
        for plugin in test.get('plugins', []):
            plugin_name = plugin.get('plugin_metadata', {}).get('plugin_name', 'Unknown')
            plugin_success[plugin_name] = plugin.get('success', False)
            
            # Extract detailed plugin information
            plugin_result = plugin.get('result', {})
            plugin_details[plugin_name] = plugin_result
            
            # Special handling for bandwidth validation plugin
            if plugin_name == 'validate_bandwidth':
                bandwidth_threshold = plugin_result.get('bandwidth_threshold_gbps', "N/A")
                bandwidth_validation_msg = plugin_result.get('validation_message', '')
            
            # Collect all plugin failure messages
            if not plugin.get('success', False):
                plugin_msg = plugin.get('msg', '')
                if plugin_msg:
                    plugin_failure_messages.append(f"{plugin_name}: {plugin_msg}")
        
        # Add plugin failure messages to error message
        if plugin_failure_messages:
            plugin_failures_text = "; ".join(plugin_failure_messages)
            if error_msg:
                error_msg += f"; {plugin_failures_text}"
            else:
                error_msg = plugin_failures_text
        
        # Calculate plugin success ratio
        total_plugins = len(plugin_success)
        successful_plugins = sum(1 for success in plugin_success.values() if success)
        plugin_success_ratio = f"{successful_plugins}/{total_plugins}" if total_plugins > 0 else "0/0"
        
        # Create row
        row = {
            'test case': test_case,
            'test type': test_type,
            'reverse': reverse,
            'success': success,
            'Plugin success': plugin_success_ratio,
            'error message': error_msg,
            'server name': server_name,
            'client name': client_name,
            'tx bitrate': tx_bitrate,
            'rx bitrate': rx_bitrate,
            'bandwidth threshold (Gbps)': bandwidth_threshold,
            'Plugin_validate_offload': plugin_success.get('validate_offload', "N/A"),
            'Plugin_measure_cpu': plugin_success.get('measure_cpu', "N/A"),
            'Plugin_measure_power': plugin_success.get('measure_power', "N/A"),
            'Plugin_validate_bandwidth': plugin_success.get('validate_bandwidth', "N/A")
        }
        
        results.append(row)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Parse test results to CSV')
    parser.add_argument('file', help='Test result file to parse')
    parser.add_argument('--csv', required=True, help='Output CSV file')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File {args.file} does not exist")
        return 1
    
    try:
        results = parse_test_file(args.file)
        df = pd.DataFrame(results)
        df.to_csv(args.csv, index=False)
        print(f"📄 Saved {len(results)} tests to {args.csv}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main()) 