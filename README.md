# Stock Data Fetcher

## Description
This Python script fetches historical trading data for listed stocks from an API and saves the data to CSV files. It is designed to help financial analysts and hobbyists analyze stock market trends.

## Features
- Fetches historical stock data including open, high, low, close, and volume values.
- Saves data in a structured CSV format within a dedicated data folder.
- Uses environment variables to securely handle sensitive information like API tokens.

## Dependencies
This project requires Python 3.x and the following Python libraries:
- `pandas`: For data manipulation and analysis.
- `requests`: For making HTTP requests to external APIs.
- `python-dotenv`: For loading environment variables from a `.env` file.

To install these dependencies, run the following command:
- pip install -r .\requirements

## Setup
1. Clone this repository or download the source code.
2. Create a `.env` file in the project root directory with the following content:
3. Replace `your_api_token_here` with your actual API token.

## Usage
Run the script using Python from the command line:

## Output
The script will fetch historical data for the tickers listed in `tickers.csv` and save them in the `data` folder as CSV files. Each file will be named after its corresponding ticker.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements.

## License
Specify your license or if the project is in the public domain.

## Contact
For any queries regarding this project, please contact [rlsandanuwan@gmail.com](mailto:rlsandanuwan@gmail.com).
