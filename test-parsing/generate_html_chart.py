#!/usr/bin/env python3
"""
Generate HTML chart from CSV test results
"""

import pandas as pd
import argparse
from pathlib import Path


def generate_html_chart(csv_file, output_file):
    """Generate HTML chart from CSV file"""
    
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Count tests with plugin failures (any plugin success ratio that's not 100%)
    def has_plugin_failures(ratio_str):
        if ratio_str == '0/0' or pd.isna(ratio_str):
            return False
        try:
            successful, total = map(int, ratio_str.split('/'))
            return successful < total
        except:
            return False
    
    plugin_failure_count = len(df[df['Plugin success'].apply(has_plugin_failures)])
    
    # Count plugin success ratios
    plugin_success_stats = df['Plugin success'].value_counts()
    
    # Create HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results Chart</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 95%;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #ddd;
        }}
        .success {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .failure {{
            color: #f44336;
            font-weight: bold;
        }}
        .warning {{
            color: #ff9800;
            font-weight: bold;
        }}
        .error-message {{
            max-width: 300px;
            word-wrap: break-word;
        }}
        .summary {{
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary h3 {{
            margin-top: 0;
            color: #2196F3;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stat-widget {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #2196F3;
        }}
        .stat-widget.total {{
            border-left-color: #2196F3;
        }}
        .stat-widget.success {{
            border-left-color: #4CAF50;
        }}
        .stat-widget.failure {{
            border-left-color: #f44336;
        }}
        .stat-widget.warning {{
            border-left-color: #ff9800;
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .stat-widget.total .stat-number {{
            color: #2196F3;
        }}
        .stat-widget.success .stat-number {{
            color: #4CAF50;
        }}
        .stat-widget.failure .stat-number {{
            color: #f44336;
        }}
        .stat-widget.warning .stat-number {{
            color: #ff9800;
        }}
        .plugin-success {{
            font-weight: bold;
        }}
        .plugin-success.0/0 {{
            color: #999;
        }}
        .plugin-success.0/1 {{
            color: #f44336;
        }}
        .plugin-success.1/1 {{
            color: #4CAF50;
        }}
        .plugin-success.2/2 {{
            color: #4CAF50;
        }}
        .plugin-success.3/3 {{
            color: #4CAF50;
        }}
        .plugin-success.4/4 {{
            color: #4CAF50;
        }}
        .plugin-success.1/2 {{
            color: #f44336;
        }}
        .plugin-success.1/3 {{
            color: #f44336;
        }}
        .plugin-success.2/3 {{
            color: #f44336;
        }}
        .plugin-success.2/4 {{
            color: #f44336;
        }}
        .plugin-success.3/4 {{
            color: #f44336;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Results Chart</h1>
        
        <div class="summary">
            <h3>Test Results Summary</h3>
            <div class="stats-grid">
                <div class="stat-widget total">
                    <div class="stat-number">{len(df)}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-widget success">
                    <div class="stat-number">{len(df[df['success'] == True])}</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-widget failure">
                    <div class="stat-number">{len(df[df['success'] == False])}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-widget warning">
                    <div class="stat-number">{plugin_failure_count}</div>
                    <div class="stat-label">Plugin Failures</div>
                </div>
                <div class="stat-widget success">
                    <div class="stat-number">{(len(df[df['success'] == True]) / len(df) * 100):.1f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Test Case</th>
                    <th>Test Type</th>
                    <th>Reverse</th>
                    <th>Success</th>
                    <th>Plugin Success</th>
                    <th>Error Message</th>
                    <th>Server Name</th>
                    <th>Client Name</th>
                    <th>TX Bitrate (Gbps)</th>
                    <th>RX Bitrate (Gbps)</th>
                    <th>Bandwidth Threshold (Gbps)</th>
                    <th>Validate Offload</th>
                    <th>Measure CPU</th>
                    <th>Measure Power</th>
                    <th>Validate Bandwidth</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Add table rows
    for _, row in df.iterrows():
        success_class = "success" if row['success'] else "failure"
        success_text = "✓" if row['success'] else "✗"
        
        # Format error message
        error_msg = str(row['error message']) if pd.notna(row['error message']) else ""
        if "WARNING" in error_msg:
            error_msg = f'<span class="warning">{error_msg}</span>'
        
        # Format plugin success ratio
        plugin_success = str(row['Plugin success'])
        plugin_success_class = plugin_success.replace('/', '')
        
        # Format plugin results
        validate_offload = "✓" if row['Plugin_validate_offload'] == True else "✗" if row['Plugin_validate_offload'] == False else "N/A"
        measure_cpu = "✓" if row['Plugin_measure_cpu'] == True else "✗" if row['Plugin_measure_cpu'] == False else "N/A"
        measure_power = "✓" if row['Plugin_measure_power'] == True else "✗" if row['Plugin_measure_power'] == False else "N/A"
        validate_bandwidth = "✓" if row['Plugin_validate_bandwidth'] == True else "✗" if row['Plugin_validate_bandwidth'] == False else "N/A"
        
        html_content += f"""
                <tr>
                    <td>{row['test case']}</td>
                    <td>{row['test type']}</td>
                    <td>{row['reverse']}</td>
                    <td class="{success_class}">{success_text}</td>
                    <td class="plugin-success {plugin_success_class}">{plugin_success}</td>
                    <td class="error-message">{error_msg}</td>
                    <td>{row['server name']}</td>
                    <td>{row['client name']}</td>
                    <td>{row['tx bitrate'] if pd.notna(row['tx bitrate']) else 'N/A'}</td>
                    <td>{row['rx bitrate'] if pd.notna(row['rx bitrate']) else 'N/A'}</td>
                    <td>{row['bandwidth threshold (Gbps)'] if pd.notna(row['bandwidth threshold (Gbps)']) else 'N/A'}</td>
                    <td>{validate_offload}</td>
                    <td>{measure_cpu}</td>
                    <td>{measure_power}</td>
                    <td>{validate_bandwidth}</td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"📊 Generated HTML chart: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate HTML chart from CSV test results')
    parser.add_argument('csv_file', help='Input CSV file')
    parser.add_argument('--output', '-o', default='test_chart.html', help='Output HTML file (default: test_chart.html)')
    
    args = parser.parse_args()
    
    if not Path(args.csv_file).exists():
        print(f"Error: CSV file {args.csv_file} does not exist")
        return 1
    
    try:
        generate_html_chart(args.csv_file, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main()) 