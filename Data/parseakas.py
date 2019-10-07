#!/usr/bin/python3

import psycopg2
import csv
import sys


def parseakas(basics, connstr):
    """
    read title.akas.tsv
    parsed data to be inputted to title_akass, title_attributes tables

    :NOTE: akas increase parsing time and does not offer useful data

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    """
    with open("title.akas.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
        csv.field_size_limit(sys.maxsize)
        # open database connection to postgres database
        try:
            conn = psycopg2.connect(connstr)
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
                    if row['titleId'] in basics:
                        if row['attributes'] is not None:
                            attributes = row['attributes'].split(' ')
                        region = row['region']
                        language = row['language']
                        isorig = row['isOriginalTitle']
                        # sets null values to null equivalent
                        if region == '\\N':
                            region = None
                        if language == '\\N':
                            language = None
                        if isorig == '\\N':
                            isorig = None
                        cur.execute("""
                            INSERT INTO title_akas
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """,
                            (row['titleId'], row['ordering'], row['title'], region, language, isorig))
                        # possible to make attributes into an array with postgres
                        # TODO: make attributes into array to simplify queries
                        num = 1
                        for att in attributes:
                            cur.execute("""
                                INSERT INTO title_attributes
                                VALUES (%s, %s, %s, %s);
                                """,
                                (row['titleId'], row['ordering'], num, att))
                            num += 1
                        print("parseakas at %s" %(row['titleId']))
            except Exception as e:
                # prints id of failed input
                print("input failed at %s in parseakas" %(row['titleId']))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parseakas" %(id))
                    log.write(str(row)+"\n")
                    log.write(str(e)+'\n')
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()
