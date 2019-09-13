LogAnalzer : Gives you the most updated set of data. Everytime

Running LogAnalzer module :

    1. Run newsdata.sql file
    2. Run LogAnalysis.py script

About LogAnalysis Module:

    On every run, this module CREATES OR REPLACE a view which is nothing but a grouped aggregation of succesful responses for each URL path.
    This view was created since same query was used in 2 parts of this Log Analyzer.

    "CREATE OR REPLACE VIEW pathCountForSuccess as " \
    "select path, count(*) as views " \
    "from log " \
    "where status like '20%' " \
    "group by path order by views desc"

Solution Explanation :

    1. Most Popular 3 Articles
        pathCountForSuccess view gives us the most visited URL
        URL is nothing but /content/slug for a particular article
        You simply need to join pathCountForSuccess with articles table on condition that slug matches the url

    2. Views generated by each author
        From problem 1, we have a new table returned which gives views on each article.
        Joining this table with authors table gives us views on each article of a author.
        Aggregate this table and we have views accumulated on all articles given by a author

    3. Days where Failed responses percentag was more than 1%
        First it creates 2 internal tables
            First table is aggregation on date of all log records whose status starts with 40 (i.e. error status)
            Second table is a aggregation on date of all log records on date.
        Then we do First left join Second on date and hence we now have a table with 3 columns : date, total responses and error responses
        Now we simply find percentages of error responses on this left join and filter the data when this percentage is greater than 1.
