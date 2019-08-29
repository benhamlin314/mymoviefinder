#!/usr/bin/python3

import psycopg2
import csv

# read title.basics.tsv
# parsed data to be inputted to title_basics, title_genre tables
# this parser must run first due to dependencies in the database

def main():
    with open("title.basics.tsv/data.tsv", "rt", newline='') as file:
        # open database connection to postgres database
        # conn = psycopg2.connect("dbname=mymoviefinder user=postgres")
        # cur = conn.cursor()
        reader = csv.DictReader(file, delimiter="\t")
        for field in reader.fieldnames:
            print(field)
        for row in reader:
            # input data in table
            print(row['tconst'], row['titleType'], row['primaryTitle'], row['originalTitle'], row['isAdult'], row['startYear'], row['endYear'], row['runtimeMinutes'], row['genres'])

if __name__ == '__main__':
    main()
