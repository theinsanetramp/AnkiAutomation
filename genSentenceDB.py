import sqlite3
from sqlite3 import Error
import csv
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_sentence(conn, sentence):
    """
    Create a new sentence into the sentences table
    :param conn:
    :param sentence:
    :return: sentence id
    """
    sql = """ INSERT INTO sentences(japanese,english)
              VALUES(?,?) """
    try:
        cur = conn.cursor()
        cur.execute(sql, sentence)
        return cur.lastrowid
    except Error as e:
        print(e)
        return None

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS sentences (
                                        id integer PRIMARY KEY,
                                        japanese text NOT NULL,
                                        english text NOT NULL
                                    ); """
 
conn = create_connection("tatoeba/japTatoeba.db")
jpnList = []
engList = []

if conn is not None:
    # create projects table
    create_table(conn, sql_create_projects_table)
    with open('tatoeba/sentences.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if row[1] == 'jpn':
                jpnList.append((int(row[0]),row[2]))
                line_count += 1
            if row[1] == 'eng':
                engList.append((int(row[0]),row[2]))
                line_count += 1
        print(f'Processed {line_count} sentences.')
    #print(create_sentence(conn, sentence))
    with open('tatoeba/links.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            iRow = (int(row[0]), int(row[1]))
            if iRow[0] > 6241747:
                for jpnSentence in jpnList:
                    if iRow[0] == jpnSentence[0]:
                        for engSentence in engList:
                            if iRow[1] == engSentence[0]:
                                create_sentence(conn, (jpnSentence[1],engSentence[1]))
                                conn.commit()
                                print(jpnSentence[1])
                                print(engSentence[1])
                                print("-"*40)
            line_count += 1
            if line_count % 1000 == 0:
                print(f'Processed {line_count} lines.')
    conn.close()
else:
    print("Error! cannot create the database connection.")