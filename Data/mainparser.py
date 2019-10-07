#!/usr/bin/python3

# import each parser
import psycopg2
from parsebasic import parsebasic
from parseakas import parseakas
from parsenames import parsenames
from parseepisodes import parseepisodes
from parseprincipals import parseprincipals
from parseratings import parseratings
from parsecrew import parsecrew

def main():
    # basics stores id of titles entered into mymoviefinder_db.title_basics
    basics = set()
    names = set()
    user = input("Please enter postgres user name (default: postgres): ")
    password = input("password: ")
    print("%s, %s" %(user, password))
    connstr = "dbname=mymoviefinder_db user="+user+" password="+password
    try:
        conn = psycopg2.connect(connstr)
        cur = conn.cursor()
    except Exception as e:
        print("failed to connect to mymoviefinder_db please try again...")
        print(e)
    else:
        cur.execute("""
            DROP TABLE title_basics, title_genre, title_akas, title_attributes, crew_names, crew_known_for, crew_professions, title_directors, title_writers, title_episodes, title_principals, title_characters, title_ratings, format, user_info CASCADE;
            """)
        cur.execute(open("create.sql", "r").read())
        conn.commit()
        cur.close()
        conn.close()
        log = open("errorlog.txt", "w")
        log.close()
        basics = parsebasic(connstr)
        if basics is not None:
            # if basic parse successful then continue parsing the other Files
            names = parsenames(basics, connstr)
            parsecrew(basics, names, connstr)
            parseepisodes(basics, connstr)
            parseprincipals(basics, names, connstr)
            parseratings(basics, connstr)


if __name__ == '__main__':
    main()
