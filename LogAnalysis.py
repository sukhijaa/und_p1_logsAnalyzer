#!/usr/bin/env python3

import psycopg2

getTop3Articles = \
    "select title, pathCountForSuccess.views " \
    "from articles, pathCountForSuccess " \
    "where pathCountForSuccess.path like CONCAT('%', articles.slug, '%') " \
    "limit 3"

getViewsPerAuthor = \
    "select authors.name, authorViewsView.authorViews " \
    "from authors, (" \
    "select articles.author, sum(pathCountForSuccess.views) as authorViews " \
    "from articles, pathCountForSuccess " \
    "where pathCountForSuccess.path like CONCAT('%',articles.slug, '%') " \
    "group by articles.author " \
    "order by authorViews desc" \
    ") as authorViewsView " \
    "where authors.id = authorViewsView.author"

getMostErrorneousDays = \
    "select errorDate, ptgErr from " \
    "(" \
    "select errorDate, " \
    "CAST(errorCounts as float)/CAST(totalCounts as float) * 100 as ptgErr " \
    "from " \
    "(" \
    "select DATE(log.time) as errorDate, count(*) as errorCounts " \
    "from log " \
    "where log.status like '40%' " \
    "group by errorDate " \
    "order by errorDate" \
    ") as errorsView " \
    "left join " \
    "(" \
    "select DATE(log.time) as totalDate, count(*) as totalCounts " \
    "from log " \
    "group by totalDate" \
    ") as totalView " \
    "on errorDate = totalDate" \
    ") as leftJoin " \
    "where ptgErr > 1 " \
    "order by ptgErr desc"


def getDBConnectionCursor():
    try:
        return psycopg2.connect(database="news")
    except psycopg2.Error as e:
        print("ERROR: Failed to connect to DB \"news\". Make sure DB exists")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)


def closeDBConnection(conn):
    conn.close()
    return


def printArticles(myCursor):
    print("Most popular 3 Articles of all time : \n")

    myCursor.execute(getTop3Articles)

    for i, row in enumerate(myCursor.fetchall()):
        print("\t{}. \"{}\" -- {} views".format(i + 1, row[0], row[1]))

    return


def printFamousAuthors(myCursor):
    print("Views garnered by each author : \n")

    myCursor.execute(getViewsPerAuthor)

    for i, row in enumerate(myCursor.fetchall()):
        print("\t{}. {} -- {} views".format(i + 1, row[0], row[1]))

    return


def printErrorneousDays(myCursor):
    print("Worst days on Network : \n")

    myCursor.execute(getMostErrorneousDays)

    for i, row in enumerate(myCursor.fetchall()):
        print("\t{}. {} -- {}% errors".format(i + 1, row[0], row[1]))

    return


if __name__ == '__main__':
    print("\nStarting to Print the Report : \n\n")
    conn = getDBConnectionCursor()
    myCursor = conn.cursor()

    printArticles(myCursor)
    print("\n\n")
    printFamousAuthors(myCursor)
    print("\n\n")
    printErrorneousDays(myCursor)

    closeDBConnection(conn)
