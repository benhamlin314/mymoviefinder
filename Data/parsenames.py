#!/usr/bin/python3

import psycopg2
import csv


def parsenames(basics, connstr):
    """
    reads name.basics.tsv
    parsed data to be inputted into crew_names, crew_known_for, crew_professions

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    :return: set containing the names entered into crew_names table
        :NOTE: set of names used for membership checking with parsecrew and parseprincipals
    """
    with open("name.basics.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
        # open database connection to postgres database
        # TODO: make user and password user input allowing for more personalization
        names = set()
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
                # flag used to prevent commit upon unsuccessful parse
                flag = False
                for row in reader:
                    name = row['primaryName']
                    id = row['nconst']
                    birthyear = row['birthYear']
                    deathyear = row['deathYear']
                    if row['knownForTitles'] is not None:
                        knownTitles = row['knownForTitles'].split(',')
                    if deathyear == '\\N':
                        deathyear = None
                    if birthyear == '\\N':
                        birthyear = None
                    if row['primaryProfession'] is not None:
                        professions = row['primaryProfession'].split(',')
                    name = row['primaryName']
                    id = row['nconst']
                    cur.execute("""
                        INSERT INTO crew_names
                        VALUES (%s, %s, %s, %s);
                        """,
                        (id, name, birthyear, deathyear))
                    for title in knownTitles:
                        # condition accounts for empty known for titles
                        if title != '\\N':
                            if title in basics:
                                cur.execute("""
                                    INSERT INTO crew_known_for
                                    VALUES (%s, %s);
                                    """,
                                    (id, title))
                    for profession in professions:
                        # condition accounts for empty profession
                        if profession != '\\N':
                            cur.execute("""
                                INSERT INTO crew_professions
                                VALUES (%s, %s);
                                """,
                                (id, profession))
                    print("parsenames at %s" %(id))
                    names.add(id)
            except Exception as e:
                # prints id of failed input
                print("input failed at %s in parsenames" %(id))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parsenames\n" %(id))
                    log.write(str(row)+"\n")
                    log.write(str(e)+'\n')
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                    cur.close()
                    conn.close()
                    return names
                else:
                    cur.close()
                    conn.close()
                    return None
