#!/usr/bin/python3

import psycopg2
import csv

# read title.akas.tsv
# parsed data to be inputted to title_akass, title_attributes tables

def main():
    with open("title.akas.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
        # open database connection to postgres database
        # TODO: make user and password user input allowing for more personalization
        try:
            conn = psycopg2.connect("dbname=mymoviefinder_db user=postgres password=1234")
            cur = conn.cursor()
        except:
            print("failed to connect to mymoviefinder_db please try again...")
        else:
            # connection to database successful
            reader = csv.DictReader(file, delimiter="\t")
            for field in reader.fieldnames:
                print(field)
            try:
                # flag prevents commit if parse fails
                flag = False
                for row in reader:
                    # input data in table
                    if row['attributes'] is not None:
                        attributes = row['attributes'].split(' ')
                    region = row['region']
                    language = row['language']
                    # sets null values to null equivalent
                    if region == '\\N':
                        region = None
                    if language == '\\N':
                        language = None
                    cur.execute("""
                        INSERT INTO title_akas
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """,
                        (row['tconst'], row['ordering'], row['title'], region, language, row['isOriginalTitle']))
                    # possible to make attributes into an array with postgres
                    # TODO: make attributes into array to simplify queries
                    for att in attributes:
                        cur.execute("""
                            INSERT INTO title_attributes
                            VALUES (%s, %s, %s);
                            """,
                            (row['tconst'], row['ordering'], att))
                    # provides feedback to user
                    print(row['tconst'])
            except Exception as e:
                # prints id of failed input
                print("input failed at %s" %(row['tconst']))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()

if __name__ == '__main__':
    main()
