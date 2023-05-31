# SQL Injection Challenge

This Python script is designed to perform a SQL Injection attack on a vulnerable website. The attack is permitted by the site creator and serves as a challenge for programmers to exploit the vulnerability.

## Prerequisites
Before running the code, ensure that you have performed the following steps:

1. Log in to the target website as user "bob".
2. Copy your session cookie.
3. Replace the value of the `PHPSESSID` cookie in the `cookies` dictionary with your copied session cookie.

## Usage
1. Set the `url` variable to the URL of the vulnerable website (e.g., `'http://localhost:8000/blindsqli.php'`).
2. Run the script.

## Description
The script provides several functions to extract information from the vulnerable database using SQL Injection. Here's an overview of each function:

### `find_table_name(url, cookies)`
Finds the name of the table in the database using SQL Injection. It iterates through ASCII characters and checks if each character is present at a specific index in the table name. If the injected query successfully executes, the string 'bobby' will be present in the response text. The function returns the found table name.

### `find_num_of_cols(url, cookies, table_name)`
Finds the number of columns in a given table name using SQL Injection. It increases a counter and checks if it matches the number of columns in the table. If the injected query succeeds, the response will contain the string 'bobby'. The function returns the number of columns in the table.

### `find_columns_name(url, cookies, table_name, num_of_cols)`
Finds the names of the columns in a given table using SQL Injection. It iterates through ASCII characters and checks if each character is present at a specific index in each column name. If the injected query succeeds, the response will contain the string 'bobby'. The function returns a list of the found column names.

### `find_num_of_rows(url, cookies, table_name)`
Finds the number of rows in a given table using SQL Injection. It increases a counter and checks if it matches the number of rows in the table. If the injected query succeeds, the response will contain the string 'bobby'. The function returns the number of rows in the table.

### `print_data(url, cookies, table_name, num_of_cols, columns, num_of_rows)`
Prints all the data from the specified table using SQL Injection. It iterates through each row and column, extracting the data character by character. The function stops when it encounters two consecutive spaces, indicating the end of the data. The extracted data is printed to the console.

## Notes
- This script assumes that the vulnerable website allows SQL Injection and returns the string 'bobby' in its response when a query succeeds.
- The script utilizes the `requests` library to send HTTP requests to the target website.
- The `string` module is used to generate the list of ASCII characters to iterate through during the SQL Injection process.
- Make sure to use this script responsibly and only on websites that explicitly permit such activities for educational or testing purposes. Unethical and unauthorized use of this script is strictly prohibited.

**Disclaimer**: The use of this script on any website without proper authorization is illegal. Use it responsibly and at your own risk.
