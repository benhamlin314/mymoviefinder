#!/usr/bin/python3

import psycopg2
import csv


def parseepisodes(basics, connstr):
    """
    read title.episode.tsv
    parsed data to be inputted to title_episodes tables

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    """
    with open("title.episode.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
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
                num = 1
                for row in reader:
                    if row['tconst'] in basics:
                        id = row['tconst']
                        parentid = row['parentTconst']
                        if parentid in basics:
                            season = row['seasonNumber']
                            episode = row['episodeNumber']
                            if season == '\\N':
                                season = None
                            if episode == '\\N':
                                episode = None
                            cur.execute("""
                                INSERT INTO title_episodes
                                VALUES (%s, %s, %s, %s, %s);
                                """,
                                (num, id, parentid, season, episode))
                            print("parseepisodes at %s" %(id))
                            num = num + 1
            except Exception as e:
                # prints id of failed input
                print("Input failed at %s in parseepisodes" %(id))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parseepisodes\n" %(id))
                    log.write(str(row)+"\n")
                    log.write(str(e)+'\n')
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()
