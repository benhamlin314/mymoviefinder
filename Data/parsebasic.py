#!/usr/bin/python3

import psycopg2
import csv



def parsebasic(connstr):
    """
    reads title.basics.tsv
    parsed data to be inputted to title_basics, title_genre tables
    this parser must run first due to dependencies in the database

    :param connstr: string for postgres database connection
    :return: array containing every titleId inputted
    """
    with open("title.basics.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
        # open database connection to postgres database
        basics = set()
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
                    # condition checks for poor reading from missing '"' in data set
                    # fixes the parse when titles are read incorrectly
                    if int(row['isAdult']) > 1:
                        titles = row['primaryTitle'].split('\t')
                        primaryTitle = titles[0]
                        secondtitle = titles[1]
                        adult = row['originalTitle']
                        startyear = row['isAdult']
                        endyear = row['startYear']
                        runtime = row['endYear']
                        genres = row['runtimeMinutes']
                        #sets null values to null equivalent
                        if endyear == "\\N":
                            endyear = None
                        if runtime == "\\N":
                            runtime = None
                        if startyear == '\\N':
                            startyear = None
                        if genres is not None:
                            genres = genres.split(',')
                        cur.execute("""
                            INSERT INTO title_basics
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                            """,
                            (row['tconst'], row['titleType'], primaryTitle, secondtitle, adult, startyear, endyear, runtime))
                        for genre in genres:
                            cur.execute("""
                                INSERT INTO title_genre
                                VALUES (%s, %s);
                                """,
                                (row['tconst'], genre))
                    else:
                        # parse read correctly
                        startyear = row['startYear']
                        endyear = row['endYear']
                        if row['genres'] is not None:
                            genres = row['genres'].split(',')
                        runtime = row['runtimeMinutes']
                        #sets null values to null equivalent
                        if endyear == "\\N":
                            endyear = None
                        if runtime == "\\N":
                            runtime = None
                        if startyear == '\\N':
                            startyear = None
                        cur.execute("""
                            INSERT INTO title_basics
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                            """,
                            (row['tconst'], row['titleType'], row['primaryTitle'], row['originalTitle'], row['isAdult'], startyear, endyear, runtime))
                        # possible to make genres into an array with postgres
                        # TODO: make genres into array to simplify queries
                        for genre in genres:
                            cur.execute("""
                                INSERT INTO title_genre
                                VALUES (%s, %s);
                                """,
                                (row['tconst'], genre))
                    print("parsebasic at %s" %(row['tconst']))
                    basics.add(row['tconst'])
            except Exception as e:
                # prints id of failed input
                print("input failed at %s in parsebasic" %(row['tconst']))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parsebasic" %(id))
                    log.write(str(row))
                    log.write(str(e))
            finally:
                # commits and closes connections to database

                if not flag:
                    conn.commit()
                    cur.close()
                    conn.close()
                    return basics
                else:
                    cur.close()
                    conn.close()
                    return None
