#!/usr/bin/python3

import psycopg2
import csv


def parseratings(basics, connstr):
    """
    read title.ratings.tsv
    parsed data to be inputted to title_directors, title_writers tables

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    """
    with open("title.ratings.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
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
                        average = row['averageRating']
                        num_votes = row['numVotes']
                        cur.execute("""
                            INSERT INTO title_ratings
                            VALUES (%s, %s, %s);
                            """,
                            (id, average, num_votes))
                        print("parseratings at %s" %(id))
            except Exception as e:
                # prints id of failed input
                print("input failed at %s in parseratings" %(row['tconst']))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parseepisodes" %(id))
                    log.write(str(row))
                    log.write(str(e))
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()
