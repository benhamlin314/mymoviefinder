#!/usr/bin/python3

import psycopg2
import csv
import re

def parsecharacter(characters):
    """
    parses the character string from the imdb dataset file title.principals.tsv
    removes segment the character is in

    :param characters: string of characters the individual had for the specific title
    :return: array of character names
    """
    char_names = []
    characters = characters.replace('[', '')
    characters = characters.replace(']', '')
    characters = characters.split(',')
    for character in characters:
        character = re.sub(' \((segments|segment) .*\)', '', character)
        char_names.append(character)
    return char_names

def parseprincipals(basics, names, connstr):
    """
    read title.principals.tsv
    parsed data to be inputted to title_episodes, title_characters tables

    :param basics: array of parsed titles committed to title_basics
    :param connstr: string for postgres connection
    """
    with open("title.principals.tsv/data.tsv", "rt", newline='', encoding='utf-8') as file:
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
                        if row['nconst'] in names:
                            titleid = row['tconst']
                            ordering = row['ordering']
                            nameid = row['nconst']
                            category = row['category']
                            job = row['job']
                            characters = row['characters']
                            characters = parsecharacter(characters)
                            # job titles greater than 255 characters long are treated as bad entry
                            if len(job) >= 255:
                                job = None
                            if job == '\\N':
                                job = None
                            cur.execute("""
                                INSERT INTO title_principals
                                VALUES (%s, %s, %s, %s, %s);
                                """,
                                (titleid, ordering, nameid, category, job))
                            num = 1
                            if characters[0]  == '\\N':
                                characters = None
                                cur.execute("""
                                    INSERT INTO title_characters
                                    VALUES (%s, %s, %s, %s, %s);
                                    """,
                                    (titleid, ordering, nameid, num, characters))
                            else:
                                for character in characters:
                                    cur.execute("""
                                        INSERT INTO title_characters
                                        VALUES (%s, %s, %s, %s, %s);
                                        """,
                                        (titleid, ordering, nameid, num, character))
                                    num += 1
                            print("parseprincipals at %s" %(titleid))
            except Exception as e:
                # prints id of failed input
                print("input failed at %s in parseprincipals" %(row['tconst']))
                # prints dictionary entry of input
                print(row)
                # prints error encountered
                print(e)
                flag = True
                with open("errorlog.txt", "a") as log:
                    log.write("Input failed at %s in parseprincipals\n" %(titleid))
                    log.write(str(row)+"\n")
                    log.write(str(e)+'\n')
            finally:
                # commits and closes connections to database
                if not flag:
                    conn.commit()
                cur.close()
                conn.close()

if __name__ == '__main__':
    characters = parsecharacter("[\"Himself - the Director of the New York Central Railroad\"]")
    print(characters[0])
    characters = parsecharacter("\\N")
    print(characters)
