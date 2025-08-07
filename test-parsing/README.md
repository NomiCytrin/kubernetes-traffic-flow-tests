# Test Result Parser

Simple tool to parse Kubernetes Traffic Flow Test results into CSV format.

## Usage

### Parse a single test result file:

```bash
cd test-parsing
python3 parse_single_file.py <result-file> --csv <output.csv>
```

**Example:**
```bash
cd test-parsing
python3 parse_single_file.py ../ft-logs/2025-07-21-10-57-22-RESULTS --csv results.csv
```

### Generate HTML chart from CSV:

```bash
python3 generate_html_chart.py <csv_file> --output <output.html>
```

**Example:**
```bash
python3 generate_html_chart.py results.csv --output test_chart.html
```

The HTML chart provides:
- Summary statistics (total tests, success rate, etc.)
- Formatted table with color-coded success/failure indicators
- Bandwidth validation warnings highlighted in orange
- Responsive design for easy viewing

## Output Format

The CSV contains the following columns:

- `test case` - Test case identifier
- `test type` - Type of test (IPERF_TCP, NETPERF_TCP_STREAM, etc.)
- `reverse` - Boolean indicating if the test was run in reverse direction
- `success` - Boolean indicating if the test passed
- `error message` - Error message if the test failed
- `server name` - Name of the server node
- `client name` - Name of the client node
- `tx bitrate` - Transmission bitrate in Gbps
- `rx bitrate` - Reception bitrate in Gbps
- `bandwidth validation` - Boolean (true for iperf tests, false for netperf tests)
- `Plugin_validate_offload` - Boolean indicating if validate_offload plugin succeeded
- `Plugin_measure_cpu` - Boolean indicating if measure_cpu plugin succeeded
- `Plugin_measure_power` - Boolean indicating if measure_power plugin succeeded

## Requirements

- Python 3.6+
- pandas

Install dependencies:
```bash
pip3 install pandas
``` 