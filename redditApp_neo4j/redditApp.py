from neo4j import GraphDatabase, RoutingControl


URI = "bolt://localhost:7687/"
AUTH = ("neo4j", "password")


def query_1():
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned alongside subreddit X")
    x = input("Subreddit X name \n >>")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (sub)-->(:Subreddit {{subredditName: '{x}'}})"
            f"MATCH (sub)-->(mentioned_sub WHERE mentioned_sub.subredditName <> '{x}')"
            f"RETURN DISTINCT mentioned_sub.subredditName;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Subreddits mentioned alongside {x}:")
        for record in records:
            print(record["mentioned_sub.subredditName"])
    print(" _ ")
    input("Press any key")


def query_2():
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned in negative way in subreddit X")
    x = input("Subreddit X name \n >>")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (:Subreddit {{subredditName: '{x}'}})-[r WHERE r.isNegative = True]->(mentioned_sub)"
            f"RETURN DISTINCT mentioned_sub.subredditName;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Subreddits mentioned negatively in {x}:")
        for record in records:
            print(record["mentioned_sub.subredditName"])
    print(" _ ")


def query_3():
    print("______ Reddit Analyzer ______")
    print("Find subreddit mentioned the most often in not negative manner:")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH ()-[r WHERE r.isNegative = False]->(mentioned_sub)"
            f"RETURN count(r) as mention_count, mentioned_sub.subredditName"
            f"ORDER BY mention_count DESC"
            f"LIMIT 1;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        for record in records:
            print(record["mentioned_sub.subredditName"], record["mention_count"])
    print(" _ ")


def query_4():
    print("______ Reddit Analyzer ______")
    print("Return X top subreddits that where mentioned the most")
    x = int(input("Number of top subreddits \n >>"))
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH ()-[r]->(mentioned_sub)"
            f"RETURN count(r) as mention_count, mentioned_sub.subredditName"
            f"ORDER BY mention_count DESC"
            f"LIMIT {x};",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"{x} top subreddits that where mentioned the most:")
        for record in records:
            print(record["mentioned_sub.subredditName"], record["mention_count"])
    print(" _ ")


def query_5():
    print("______ Reddit Analyzer ______")
    print("Find subreddit with the most posts with LIWC_X > 0")
    x = input("Which LIWC (\n1. LIWC_Swear, \n2. LIWC_Anger, \n3. LIWC_Sad, \n4. LIWC_Dissent) \n >>")
    int_to_liwc = {
        "1": "swear",
        "2": "anger",
        "3": "sad",
        "4": "dissent",
    }
    x = int_to_liwc[x]
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (sub)-[r WHERE r.{x} > 0]->()"
            f"RETURN count(r) as posts_count, sub.subredditName"
            f"ORDER BY posts_count DESC"
            f"LIMIT 1;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Subreddit with the most posts with LIWC_{x}:")
        for record in records:
            print(record["sub.subredditName"], record["posts_count"])
    print(" _ ")


def query_6():
    print("______ Reddit Analyzer ______")
    print("Find all subreddits mentioned in subreddits mentioned in subreddit X (neighbours of neighbours of X)")
    x = input("Subreddit X name \n >>")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (:Subreddit {{subredditName: '{x}'}})-->(neighbour_sub)"
            f"MATCH (neighbour_sub)-->(neighbour_of_neighbour)"
            f"RETURN DISTINCT neighbour_of_neighbour.subredditName;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Neighbours of neighbours of {x}:")
        for record in records:
            print(record["neighbour_of_neighbour.subredditName"])
    print(" _ ")


def query_7():
    print("______ Reddit Analyzer ______")
    print("From subreddits mentioned in subreddit X, select subreddits which mentioned subreddit X")
    x = input("Subreddit X name \n >>")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (:Subreddit {{subredditName: '{x}'}})-->(neighbour_sub)"
            f"MATCH (neighbour_sub)-->(:Subreddit {{subredditName: '{x}'}})"
            f"RETURN DISTINCT neighbour_sub.subredditName;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Subreddits mentioned in {x}, that mentioned {x} back:")
        for record in records:
            print(record["neighbour_sub.subredditName"])
    print(" _ ")


def query_8():
    print("______ Reddit Analyzer ______")
    print("For each subreddit mentioned in subreddit X, decide "
          "if it is generally mentioned more often as negative or not-negative")
    x = input("Subreddit X name \n >>")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            f"MATCH (:Subreddit {{subredditName: '{x}'}})-->(neighbour_sub)"
            f"MATCH ()-[r_neg:TITLE_HYPERLINK {{isNegative: True}}]->(neighbour_sub)"
            f"MATCH ()-[r_pos:TITLE_HYPERLINK {{isNegative: False}}]->(neighbour_sub)"
            f"RETURN neighbour_sub.subredditName, count(distinct r_neg) as neg, count(distinct r_pos) as pos;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
        print(f"Subreddits mentioned in {x} and their negativity:")
        for record in records:
            print(record["neighbour_sub.subredditName"], record["neg"], record["pos"])
    print(" _ ")


def benchmark():
    avg_bench = 0
    for l in range(0, 6):
        print(f" Benchmark Run {l}")

        # 1
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (sub)-->(:Subreddit {{subredditName: 'leagueoflegends'}}) "
                f"MATCH (sub)-->(mentioned_sub WHERE mentioned_sub.subredditName <> 'leagueoflegends') "
                f"RETURN DISTINCT mentioned_sub.subredditName;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 1: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 1 time: {avg_bench / 5} ms")

    avg_bench = 0
    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 2
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (:Subreddit {{subredditName: 'leagueoflegends'}})-[r WHERE r.isNegative = True]->(mentioned_sub) "
                f"RETURN DISTINCT mentioned_sub.subredditName;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 2: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 2 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 3
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH ()-[r WHERE r.isNegative = False]->(mentioned_sub) "
                f"RETURN count(r) as mention_count, mentioned_sub.subredditName "
                f"ORDER BY mention_count DESC "
                f"LIMIT 1;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 3: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 3 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 4
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH ()-[r]->(mentioned_sub) "
                f"RETURN count(r) as mention_count, mentioned_sub.subredditName "
                f"ORDER BY mention_count DESC "
                f"LIMIT 10;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 4: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 4 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 5
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (sub)-[r WHERE r.swear > 0]->() "
                f"RETURN count(r) as posts_count, sub.subredditName "
                f"ORDER BY posts_count DESC "
                f"LIMIT 1;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 5: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 5 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 6
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (:Subreddit {{subredditName: 'leagueoflegends'}})-->(neighbour_sub) "
                f"MATCH (neighbour_sub)-->(neighbour_of_neighbour) "
                f"RETURN DISTINCT neighbour_of_neighbour.subredditName;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 6: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 6 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 7
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (:Subreddit {{subredditName: 'leagueoflegends'}})-->(neighbour_sub) "
                f"MATCH (neighbour_sub)-->(:Subreddit {{subredditName: 'leagueoflegends'}}) "
                f"RETURN DISTINCT neighbour_sub.subredditName;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 7: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 7 time: {avg_bench / 5} ms")

    avg_bench = 0

    for l in range(0, 6):
        print(f" Benchmark Run {l}")
        # 8
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            records, summary, _ = driver.execute_query(
                f"MATCH (:Subreddit {{subredditName: 'leagueoflegends'}})-->(neighbour_sub) "
                f"MATCH ()-[r_neg:TITLE_HYPERLINK {{isNegative: True}}]->(neighbour_sub) "
                f"MATCH ()-[r_pos:TITLE_HYPERLINK {{isNegative: False}}]->(neighbour_sub) "
                f"RETURN neighbour_sub.subredditName, count(distinct r_neg) as neg, count(distinct r_pos) as pos;",
                database_="neo4j", routing_=RoutingControl.READ,
            )
        avail = summary.result_available_after
        cons = summary.result_consumed_after
        total_time = avail + cons
        print(f"Query time 8: {total_time}")
        if l != 0:
            avg_bench += total_time

    print(f"Average query 8 time: {avg_bench / 5} ms")



if __name__ == '__main__':
    while True:
        print("______ Reddit Analyzer ______")
        print("1. Select all subreddits mentioned alongside subreddit X")
        print("2. Select all subreddits mentioned in negative way in subreddit X")
        print("3. Find subreddit mentioned the most often in not negative manner")
        print("4. Return X top subreddits that where mentioned the most")
        print("5. Find subreddit with the most posts with LIWC_X > 0")
        print("6. Find all subreddits mentioned in subreddits mentioned in subreddit X (neighbours of neighbours of X)")
        print("7. From subreddits mentioned in subreddit X, select subreddits which mentioned subreddit X")
        print("8. For each subreddit mentioned in subreddit X, decide if it is generally mentioned more often as negative or not-negative")
        print("9. Benchmark")
        print("0. Exit")
        print("_____________________________")

        i = input(">>")

        if i == "1":
            query_1()
        elif i == "2":
            query_2()
        elif i == "3":
            query_3()
        elif i == "4":
            query_4()
        elif i == "5":
            query_5()
        elif i == "6":
            query_6()
        elif i == "7":
            query_7()
        elif i == "8":
            query_8()
        elif i == "9":
            benchmark()
        elif i == "0":
            break
        else:
            print("Not recognized value.")
    print("Closing App")

