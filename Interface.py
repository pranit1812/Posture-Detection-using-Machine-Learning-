#!/usr/bin/python2.7
#
# Interface for the assignment
#
# Author: Pranit Sehgal
# ASU ID : 1225456193 

import psycopg2

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def loadRatings(ratingstablename, ratingsfilepath, openconnection):
    cur = openconnection.cursor()
    table_creation_query = (
        "DROP TABLE IF EXISTS {0};"
        "CREATE TABLE {0} ("
        "    userid INTEGER,"
        "    temp1 CHAR,"
        "    movieid INTEGER,"
        "    temp2 CHAR,"
        "    rating FLOAT,"
        "    temp3 CHAR,"
        "    Timestamp BIGINT"
        ");"
    ).format(ratingstablename)
    try:
        cur.execute(table_creation_query)
        cur.copy_from(open(ratingsfilepath), ratingstablename, sep=':')
        cur.execute("ALTER TABLE {0} DROP COLUMN temp1, DROP COLUMN temp2, DROP COLUMN temp3, DROP COLUMN Timestamp;".format(ratingstablename))
    except Exception as e:
        print("Error while processing Ratings table. Error: {0}".format(e))
    cur.close()
    openconnection.commit()


def rangePartition(ratingstablename, numberofpartitions, openconnection):
    cur = openconnection.cursor()
    partitionSize = 5.0 / numberofpartitions
    for i in range(numberofpartitions):
        start = i * partitionSize
        end = (i + 1) * partitionSize
        table_name = 'range_part{}'.format(i)
        if i == 0:
            query = (
                "CREATE TABLE {0} AS SELECT * FROM {1} "
                "WHERE rating >= {2} AND rating <= {3};"
            ).format(table_name, ratingstablename, start, end)
        else:
            query = (
                "CREATE TABLE {0} AS SELECT * FROM {1} "
                "WHERE rating > {2} AND rating <= {3};"
            ).format(table_name, ratingstablename, start, end)
        cur.execute(query)
    cur.close()
    openconnection.commit()


def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
    cur = openconnection.cursor()
    for i in range(numberofpartitions):
        tableName = 'rrobin_part{}'.format(i)
        cur.execute("DROP TABLE IF EXISTS {};".format(tableName))
        cur.execute("CREATE TABLE {} (userid INTEGER, movieid INTEGER, rating FLOAT);".format(tableName))
        cur.execute("""
            INSERT INTO {} (userid, movieid, rating)
            SELECT userid, movieid, rating 
            FROM (
                SELECT userid, movieid, rating, ROW_NUMBER() OVER() AS rnum
                FROM {}
            ) AS t1
            WHERE MOD(t1.rnum - 1, {}) = {};
        """.format(tableName, ratingstablename, numberofpartitions, i))
    cur.close()
    openconnection.commit()

def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    cur = openconnection.cursor()
    # Assuming you have a function called count_partitions
    partition_count = count_partitions("rrobin_part", openconnection)
    tableName = 'rrobin_part{}'.format(partition_count % partition_count)
    cur.execute("INSERT INTO {}(userid, movieid, rating) VALUES ({}, {}, {});".format(tableName, userid, itemid, rating))
    cur.execute("INSERT INTO {}(userid, movieid, rating) VALUES({}, {}, {});".format(ratingstablename, userid, itemid, rating))
    cur.close()
    openconnection.commit()

def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
    cur = openconnection.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name LIKE 'range_part%' AND 
        table_schema NOT IN ('information_schema', 'pg_catalog') AND
        table_type = 'BASE TABLE';
    """)
    numPartitions = int(cur.fetchall()[0][0])
    partitionSize = 5.0 / numPartitions
    partitionId = min(int(rating / partitionSize), numPartitions - 1)
    cur.execute("INSERT INTO range_part{}(userid, movieid, rating) VALUES ({}, {}, {})".format(partitionId, userid, itemid, rating))
    cur.close()
    openconnection.commit()


def createDB(dbname='dds_assignment'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print 'A database named {0} already exists'.format(dbname)

    # Clean up
    cur.close()
    con.close()

def deletepartitionsandexit(openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    l = []
    for row in cur:
        l.append(row[0])
    for tablename in l:
        cur.execute("drop table if exists {0} CASCADE".format(tablename))

    cur.close()

def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
        sys.exit(1)
    except IOError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()


