# Site Checker

[🇷🇺 Читать на русском](README_RU.md)

A script for automated subdomain existence checking based on a base URL. The script generates all possible subdomain combinations of a given length, checks their availability, and logs working links to a file.

## Description

This script uses a brute-force method to check for subdomain existence for a given base URL. It generates all possible character combinations for each subdomain level and checks their availability using HTTP requests.

### Features:
- Subdomain availability checking.
- Subdomain generation using Latin letters and digits.
- Resumes checking from the last stopped point (saves state to `progress.txt`).
- Logs working subdomains to `working_links_with_titles.txt`.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `argparse`
  - `BeautifulSoup4`
  - `aiohttp`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/site_checker.git
    cd site_checker
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the required parameters. If the `--base-url` parameter is not specified, the default URL (`narod.ru`) will be used.

### Example:
``bash
python main.py --base-url example.com
```
### Parameters:
`--base-url` - Base URL for subdomain checking. Default is narod.ru.
### Working Files:
`progress.txt` - Contains the current execution progress to resume from where the script was interrupted.
`working_links_with_titles.txt` - File to store working subdomains.
Example Output:
```bash
Starting checks for length 5
[+] Found working link: https://aaaaa.narod.ru/, Title: example
[+] Found working link: https://bbbbb.narod.ru/, Title: bbbbb
...
```
## Notes
The script uses a brute-force strategy, generating all possible combinations of letters and digits for subdomains of a given length. Each run increments the subdomain length.
## License
This project is licensed under GPLv3. See the [LICENSE](LICENSE) file for details.
