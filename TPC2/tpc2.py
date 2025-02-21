import sys
import re

first_column = re.compile(r"^([^;]*);")
first_two_columns = re.compile(r"^([^;]*);([^;]*);")
last_four_columns = re.compile(r"([^;]*;[^;]*;[^;]*;[^;]*$)")
last_column = re.compile(r"([^;]*;$)")

def read_fixed_lines(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()  #reads the whole file, keeping valid newlines intact

    fixed_lines = []
    temp_line = ""

    for line in lines:
        temp_line += line  #append line to buffer

        #count quotes to check if unbalanced/multiline field
        if temp_line.count('"') % 2 == 0:  
            fixed_lines.append(temp_line)  #full row captured
            temp_line = ""  #reset buffer

    return fixed_lines[1:] #ignore header

def parse(file):
    csv = read_fixed_lines(file)

    period_counter = {}
    period_titles = {}
    composer_set = set()

    for line in csv:
        #find title
        title = re.match(first_column, line).group(0).rstrip(";")
        #print(title)

        #skip desc column, start from end of line to grab period and composer
        last_four = re.search(last_four_columns, line).group(0)
        #print(last_four)
        period_and_composer = re.search(first_two_columns, last_four).group(0)
        #print(period_and_composer)
        period = re.search(first_column, period_and_composer).group(0).rstrip(";")
        composer = re.search(last_column, period_and_composer).group(0).rstrip(";")
        #print(period)
        #print(composer)
        composer_set.add(composer)

        #increment period counter
        if period not in period_counter:
            period_counter[period] = 1
        else:
            period_counter[period] += 1

        #add title to period/title dictionary
        if period not in period_titles:
            period_titles[period] = []
        period_titles[period].append(title)

    sorted_composers = sorted(composer_set)
    write_composers(composer_set)
    write_period_distribution(period_counter)
    write_period_dictionary(period_titles)


def write_composers(composer_set):
    with open("compositores.txt", 'w', encoding='utf-8') as result:
        for composer in sorted(composer_set):
            result.write(composer + "\n")

def write_period_distribution(period_counter, encoding='utf-8'):
    with open("distribuicao.txt", 'w') as result:
        for period, count in period_counter.items():
            result.write(f"{period}: {count}\n")

def write_period_dictionary(period_titles, encoding='utf-8'):
    with open("dicionario.txt", 'w') as result:
        for period, titles in period_titles.items():
            result.write(f"{period}:\n")
            for title in titles:
                result.write(f"  {title}\n")

if __name__ == '__main__':
    parse("obras.csv")