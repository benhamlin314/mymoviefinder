#!/usr/bin/python3

import psycopg2
import csv
import sys


def parsecrew(basics, names, connstr):
    """
    read title.crew.tsv
    parsed data to be inputted to title_directors, title_writers tables

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    """
    with open("title.crew.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
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
                    if row['tconst'] in basics:
                        id = row['tconst']
                        directors = row['directors']
                        writers = row['writers']
                        if row['directors'] is not None:
                            directors = row['directors'].split(',')
                        if row['writers'] is not None:
                            writers = row['writers'].split(',')
                        if directors == '\\N':
                            directors = None
                        else:
                            for director in directors:
                                if director in names:
                                    cur.execute("""
                                        INSERT INTO title_directors
                                        VALUES (%s, %s);
                                        """,
                                        (id, director))
                        if writers == '\\N':
                            writers = None
                        else:
                            for writ in writers:
                                if writ in names:
                                    cur.execute("""
                                        INSERT INTO title_writers
                                        VALUES (%s, %s);
                                        """,
                                        (id, writ))
                        print("parsecrew at %s" %(id))
            except Exception as e:
                # prints id of failed input
                print("Input failed at %s in parsecrew" %(id))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parsecrew\n" %(id))
                    log.write(str(row)+"\n")
                    log.write(str(e)+'\n')
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()
