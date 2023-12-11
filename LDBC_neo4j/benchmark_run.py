from neo4j import GraphDatabase, RoutingControl

URI = "bolt://localhost:7687/"
AUTH = ("neo4j", "password")

substitution_parameter_directory = f"sub0.1"    # 0.1, 0.3, 1.0, 3.0
avg_bench = 0

for i in range(0, 6):

    print(f" Benchmark Run {i}")
    benchmark_total_time = 0

    # 1
    file1 = open(f'{substitution_parameter_directory}/interactive_1_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            firstName = attr[1][:-1]
            records, summary, _ = driver.execute_query(
                f"MATCH (p:Person {{id: '{personId}'}}), (friend:Person {{firstName: '{firstName}'}}) "
                f"WHERE NOT p=friend "
                f"WITH p, friend "
                f"MATCH path = shortestPath((p)-[:KNOWS*1..3]-(friend)) "
                f"WITH min(length(path)) AS distance, friend "
                f"ORDER BY "
                f"distance ASC, "
                f"friend.lastName ASC, "
                f"toInteger(friend.id) ASC "
                f"LIMIT 20 "
                f" "
                f"MATCH (friend)-[:IS_LOCATED_IN]->(friendCity:Place) "
                f"OPTIONAL MATCH (friend)-[studyAt:STUDY_AT]->(uni:Organisation)-[:IS_LOCATED_IN]->(uniCity:Place) "
                f"WITH friend, collect( "
                f"    CASE uni.name "
                f"        WHEN null THEN null "
                f"        ELSE [uni.name, studyAt.classYear, uniCity.name] "
                f"    END ) AS unis, friendCity, distance "
                f" "
                f"OPTIONAL MATCH (friend)-[workAt:WORK_AT]->(company:Company)-[:IS_LOCATED_IN]->(companyCountry:Place) "
                f"WITH friend, collect( "
                f"    CASE company.name "
                f"        WHEN null THEN null "
                f"        ELSE [company.name, workAt.workFrom, companyCountry.name] "
                f"    END ) AS companies, unis, friendCity, distance "
                f"RETURN "
                f"    friend.id AS friendId, "
                f"    friend.lastName AS friendLastName, "
                f"    distance AS distanceFromPerson, "
                f"    friend.birthday AS friendBirthday, "
                f"    friend.creationDate AS friendCreationDate, "
                f"    friend.gender AS friendGender, "
                f"    friend.browserUsed AS friendBrowserUsed, "
                f"    friend.locationIP AS friendLocationIp, "
                f"    friend.email AS friendEmails, "
                f"    friend.speaks AS friendLanguages, "
                f"    friendCity.name AS friendCityName, "
                f"    unis AS friendUniversities, "
                f"    companies AS friendCompanies "
                f"ORDER BY "
                f"    distanceFromPerson ASC, "
                f"    friendLastName ASC, "
                f"    toInteger(friendId) ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 1: {sum_time} ms")
    benchmark_total_time += sum_time

    # 2
    file1 = open(f'{substitution_parameter_directory}/interactive_2_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            maxDate = attr[1][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (:Person {{id: '{personId}' }})-[:KNOWS]-(friend:Person)<-[:HAS_CREATOR]-(message:Message) "
                f"    WHERE message.creationDate <= {maxDate} "
                f"    RETURN "
                f"        friend.id AS personId, "
                f"        friend.firstName AS personFirstName, "
                f"        friend.lastName AS personLastName, "
                f"        message.id AS postOrCommentId, "
                f"        coalesce(message.content,message.imageFile) AS postOrCommentContent, "
                f"        message.creationDate AS postOrCommentCreationDate "
                f"    ORDER BY "
                f"        postOrCommentCreationDate DESC, "
                f"        toInteger(postOrCommentId) ASC "
                f"    LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 2: {sum_time} ms")
    benchmark_total_time += sum_time

    # 3
    file1 = open(f'{substitution_parameter_directory}/interactive_3_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            startDate = int(attr[1])
            durationDays = int(attr[2]) * 1000 * 3600 * 24
            endDate = startDate + durationDays
            countryXName = attr[3]
            countryYName = attr[4][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (countryX:Place {{name: '{countryXName}' }}), "
                f"      (countryY:Place {{name: '{countryYName}' }}), "
                f"      (person:Person {{id: '{personId}' }}) "
                f"WITH person, countryX, countryY "
                f"LIMIT 1 "
                f"MATCH (city:Place)-[:IS_PART_OF]->(country:Place) "
                f"WHERE country IN [countryX, countryY] "
                f"WITH person, countryX, countryY, collect(city) AS cities "
                f"MATCH (person)-[:KNOWS*1..2]-(friend)-[:IS_LOCATED_IN]->(city) "
                f"WHERE NOT person=friend AND NOT city IN cities "
                f"WITH DISTINCT friend, countryX, countryY "
                f"MATCH (friend)<-[:HAS_CREATOR]-(message), "
                f"      (message)-[:IS_LOCATED_IN]->(country) "
                f"WHERE {endDate} > message.creationDate >= {startDate} AND "
                f"      country IN [countryX, countryY] "
                f"WITH friend, "
                f"     CASE WHEN country=countryX THEN 1 ELSE 0 END AS messageX, "
                f"     CASE WHEN country=countryY THEN 1 ELSE 0 END AS messageY "
                f"WITH friend, sum(messageX) AS xCount, sum(messageY) AS yCount "
                f"WHERE xCount>0 AND yCount>0 "
                f"RETURN friend.id AS friendId, "
                f"       friend.firstName AS friendFirstName, "
                f"       friend.lastName AS friendLastName, "
                f"       xCount, "
                f"       yCount, "
                f"       xCount + yCount AS xyCount "
                f"ORDER BY xyCount DESC, friendId ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 3: {sum_time} ms")
    benchmark_total_time += sum_time

    # 4
    file1 = open(f'{substitution_parameter_directory}/interactive_4_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            startDate = int(attr[1])
            durationDays = int(attr[2][:-1]) * 1000 * 3600 * 24
            endDate = startDate + durationDays

            records, summary, _ = driver.execute_query(
                f"MATCH (person:Person {{id: '{personId}' }})-[:KNOWS]-(friend:Person), "
                f"      (friend)<-[:HAS_CREATOR]-(post:Post)-[:HAS_TAG]->(tag) "
                f"WITH DISTINCT tag, post "
                f"WITH tag, "
                f"     CASE "
                f"       WHEN {startDate} <= post.creationDate < {endDate} THEN 1 "
                f"       ELSE 0 "
                f"     END AS valid, "
                f"     CASE "
                f"       WHEN post.creationDate < {startDate} THEN 1 "
                f"       ELSE 0 "
                f"     END AS inValid "
                f"WITH tag, sum(valid) AS postCount, sum(inValid) AS inValidPostCount "
                f"WHERE postCount>0 AND inValidPostCount=0 "
                f"RETURN tag.name AS tagName, postCount "
                f"ORDER BY postCount DESC, tagName ASC "
                f"LIMIT 10",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 4: {sum_time} ms")
    benchmark_total_time += sum_time

    # 5
    file1 = open(f'{substitution_parameter_directory}/interactive_5_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            minDate = attr[1][:-1]
            records, summary, _ = driver.execute_query(
                f"MATCH (person:Person {{ id: '{personId}' }})-[:KNOWS*1..2]-(friend) "
                f"WHERE "
                f"    NOT person=friend "
                f"WITH DISTINCT friend "
                f"MATCH (friend)<-[membership:HAS_MEMBER]-(forum) "
                f"WHERE "
                f"    membership.joinDate > {minDate} "
                f"WITH "
                f"    forum, "
                f"    collect(friend) AS friends "
                f"OPTIONAL MATCH (friend)<-[:HAS_CREATOR]-(post)<-[:CONTAINER_OF]-(forum) "
                f"WHERE "
                f"    friend IN friends "
                f"WITH "
                f"    forum, "
                f"    count(post) AS postCount "
                f"RETURN "
                f"    forum.title AS forumName, "
                f"    postCount "
                f"ORDER BY "
                f"    postCount DESC, "
                f"    forum.id ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 5: {sum_time} ms")
    benchmark_total_time += sum_time

    # 6
    file1 = open(f'{substitution_parameter_directory}/interactive_6_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            tagName = attr[1][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (knownTag:Tag {{ name: '{tagName}' }}) "
                f"WITH knownTag.id as knownTagId "
                f"MATCH (person:Person {{ id: '{personId}' }})-[:KNOWS*1..2]-(friend) "
                f"WHERE NOT person=friend "
                f"WITH "
                f"    knownTagId, "
                f"    collect(distinct friend) as friends "
                f"UNWIND friends as f "
                f"    MATCH (f)<-[:HAS_CREATOR]-(post:Post), "
                f"          (post)-[:HAS_TAG]->(t:Tag{{id: knownTagId}}), "
                f"          (post)-[:HAS_TAG]->(tag:Tag) "
                f"    WHERE NOT t = tag "
                f"    WITH "
                f"        tag.name as tagName, "
                f"        count(post) as postCount "
                f"RETURN "
                f"    tagName, "
                f"    postCount "
                f"ORDER BY "
                f"    postCount DESC, "
                f"    tagName ASC "
                f"LIMIT 10",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 6: {sum_time} ms")
    benchmark_total_time += sum_time

    # 7
    file1 = open(f'{substitution_parameter_directory}/interactive_7_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            personId = line[:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (person:Person {{id: '{personId}'}})<-[:HAS_CREATOR]-(message:Message)<-[like:LIKES]-(liker:Person) "
                f"    WITH liker, message, like.creationDate AS likeTime, person "
                f"    ORDER BY likeTime DESC, toInteger(message.id) ASC "
                f"    WITH liker, head(collect({{msg: message, likeTime: likeTime}})) AS latestLike, person "
                f"RETURN "
                f"    liker.id AS personId, "
                f"    liker.firstName AS personFirstName, "
                f"    liker.lastName AS personLastName, "
                f"    latestLike.likeTime AS likeCreationDate, "
                f"    latestLike.msg.id AS commentOrPostId, "
                f"    coalesce(latestLike.msg.content, latestLike.msg.imageFile) AS commentOrPostContent, "
                f"    toInteger(floor(toFloat(latestLike.likeTime - latestLike.msg.creationDate)/1000.0)/60.0) AS minutesLatency, "
                f"    not((liker)-[:KNOWS]-(person)) AS isNew "
                f"ORDER BY "
                f"    likeCreationDate DESC, "
                f"    toInteger(personId) ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 7: {sum_time} ms")
    benchmark_total_time += sum_time

    # 8
    file1 = open(f'{substitution_parameter_directory}/interactive_8_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            personId = line[:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (start:Person {{id: '{personId}'}})<-[:HAS_CREATOR]-(:Message)<-[:REPLY_OF]-(comment:Comment)-[:HAS_CREATOR]->(person:Person) "
                f"RETURN "
                f"    person.id AS personId, "
                f"    person.firstName AS personFirstName, "
                f"    person.lastName AS personLastName, "
                f"    comment.creationDate AS commentCreationDate, "
                f"    comment.id AS commentId, "
                f"    comment.content AS commentContent "
                f"ORDER BY "
                f"    commentCreationDate DESC, "
                f"    commentId ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 8: {sum_time} ms")
    benchmark_total_time += sum_time

    # 9
    file1 = open(f'{substitution_parameter_directory}/interactive_9_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            maxDate = attr[1][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (root:Person {{id: '{personId}' }})-[:KNOWS*1..2]-(friend:Person) "
                f"WHERE NOT friend = root "
                f"WITH collect(distinct friend) as friends "
                f"UNWIND friends as friend "
                f"    MATCH (friend)<-[:HAS_CREATOR]-(message:Message) "
                f"    WHERE message.creationDate < {maxDate} "
                f"RETURN "
                f"    friend.id AS personId, "
                f"    friend.firstName AS personFirstName, "
                f"    friend.lastName AS personLastName, "
                f"    message.id AS commentOrPostId, "
                f"    coalesce(message.content,message.imageFile) AS commentOrPostContent, "
                f"    message.creationDate AS commentOrPostCreationDate "
                f"ORDER BY "
                f"    commentOrPostCreationDate DESC, "
                f"    message.id ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 9: {sum_time} ms")
    benchmark_total_time += sum_time

    # 10
    file1 = open(f'{substitution_parameter_directory}/interactive_10_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            month = attr[1][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH (person:Person {{id: '{personId}'}})-[:KNOWS*2..2]-(friend), "
                f"       (friend)-[:IS_LOCATED_IN]->(city:Place) "
                f"WHERE NOT friend=person AND "
                f"      NOT (friend)-[:KNOWS]-(person) "
                f"WITH person, city, friend, datetime({{epochMillis: friend.birthday}}) as birthday "
                f"WHERE  (birthday.month={month} AND birthday.day>=21) OR "
                f"        (birthday.month=({month}%12)+1 AND birthday.day<22) "
                f"WITH DISTINCT friend, city, person "
                f"OPTIONAL MATCH (friend)<-[:HAS_CREATOR]-(post:Post) "
                f"WITH friend, city, collect(post) AS posts, person "
                f"WITH friend, "
                f"     city, "
                f"     size(posts) AS postCount, "
                f"     size([p IN posts WHERE (p)-[:HAS_TAG]->()<-[:HAS_INTEREST]-(person)]) AS commonPostCount "
                f"RETURN friend.id AS personId, "
                f"       friend.firstName AS personFirstName, "
                f"       friend.lastName AS personLastName, "
                f"       commonPostCount - (postCount - commonPostCount) AS commonInterestScore, "
                f"       friend.gender AS personGender, "
                f"       city.name AS personCityName "
                f"ORDER BY commonInterestScore DESC, personId ASC "
                f"LIMIT 10",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 10: {sum_time} ms")
    benchmark_total_time += sum_time

    # 11
    file1 = open(f'{substitution_parameter_directory}/interactive_11_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            countryName = attr[1]
            workFromYear = attr[2][:-1]
            records, summary, _ = driver.execute_query(
                f"MATCH (person:Person {{id: '{personId}' }})-[:KNOWS*1..2]-(friend:Person) "
                f"WHERE not(person=friend) "
                f"WITH DISTINCT friend "
                f"MATCH (friend)-[workAt:WORK_AT]->(company:Company)-[:IS_LOCATED_IN]->(:Place {{name: '{countryName}' }}) "
                f"WHERE workAt.workFrom < {workFromYear} "
                f"RETURN "
                f"        friend.id AS personId, "
                f"        friend.firstName AS personFirstName, "
                f"        friend.lastName AS personLastName, "
                f"        company.name AS organizationName, "
                f"        workAt.workFrom AS organizationWorkFromYear "
                f"ORDER BY "
                f"        organizationWorkFromYear ASC, "
                f"        toInteger(personId) ASC, "
                f"        organizationName DESC "
                f"LIMIT 10",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 11: {sum_time} ms")
    benchmark_total_time += sum_time

    # 12
    file1 = open(f'{substitution_parameter_directory}/interactive_12_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for line in Lines:
            attr = line.split("|")
            personId = attr[0]
            tagClassName = attr[1][:-1]
            records, summary, _ = driver.execute_query(
                f"MATCH (tag:Tag)-[:HAS_TYPE|IS_SUBCLASS_OF*0..]->(baseTagClass:TagClass) "
                f"WHERE tag.name = '{tagClassName}' OR baseTagClass.name = '{tagClassName}' "
                f"WITH collect(tag.id) as tags "
                f"MATCH (:Person {{id: '{personId}' }})-[:KNOWS]-(friend:Person)<-[:HAS_CREATOR]-(comment:Comment)-[:REPLY_OF]->(:Post)-[:HAS_TAG]->(tag:Tag) "
                f"WHERE tag.id in tags "
                f"RETURN "
                f"    friend.id AS personId, "
                f"    friend.firstName AS personFirstName, "
                f"    friend.lastName AS personLastName, "
                f"    collect(DISTINCT tag.name) AS tagNames, "
                f"    count(DISTINCT comment) AS replyCount "
                f"ORDER BY "
                f"    replyCount DESC, "
                f"    toInteger(personId) ASC "
                f"LIMIT 20",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 12: {sum_time} ms")
    benchmark_total_time += sum_time

    # 13
    file1 = open(f'{substitution_parameter_directory}/interactive_13_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            attr = line.split("|")
            person1Id = attr[0]
            person2Id = attr[1][:-1]
            records, summary, _ = driver.execute_query(
                f"MATCH "
                f"    (person1:Person {{id: '{person1Id}'}}), "
                f"    (person2:Person {{id: '{person2Id}'}}), "
                f"    path = shortestPath((person1)-[:KNOWS*]-(person2)) "
                f"RETURN "
                f"    CASE path IS NULL "
                f"        WHEN true THEN -1 "
                f"        ELSE length(path) "
                f"    END AS shortestPathLength",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 13: {sum_time} ms")
    benchmark_total_time += sum_time

    # 14
    file1 = open(f'{substitution_parameter_directory}/interactive_14_param.txt', 'r')
    Lines = file1.readlines()
    sum_time = 0
    with GraphDatabase.driver(URI, auth=AUTH) as driver:

        for line in Lines:
            attr = line.split("|")
            person1Id = attr[0]
            person2Id = attr[1][:-1]

            records, summary, _ = driver.execute_query(
                f"MATCH path = allShortestPaths((person1:Person {{ id: '{person1Id}' }})-[:KNOWS*0..]-(person2:Person {{ id: '{person2Id}' }})) "
                f"WITH collect(path) as paths "
                f"UNWIND paths as path "
                f"WITH path, relationships(path) as rels_in_path "
                f"WITH "
                f"    [n in nodes(path) | n.id ] as personIdsInPath, "
                f"    [r in rels_in_path | "
                f"        reduce(w=0.0, v in [ "
                f"            (a:Person)<-[:HAS_CREATOR]-(:Comment)-[:REPLY_OF]->(:Post)-[:HAS_CREATOR]->(b:Person) "
                f"            WHERE "
                f"                (a.id = startNode(r).id and b.id=endNode(r).id) OR (a.id=endNode(r).id and b.id=startNode(r).id) "
                f"            | 1.0] | w+v) "
                f"    ] as weight1, "
                f"    [r in rels_in_path | "
                f"        reduce(w=0.0,v in [ "
                f"        (a:Person)<-[:HAS_CREATOR]-(:Comment)-[:REPLY_OF]->(:Comment)-[:HAS_CREATOR]->(b:Person) "
                f"        WHERE "
                f"                (a.id = startNode(r).id and b.id=endNode(r).id) OR (a.id=endNode(r).id and b.id=startNode(r).id) "
                f"        | 0.5] | w+v) "
                f"    ] as weight2 "
                f"WITH "
                f"    personIdsInPath, "
                f"    reduce(w=0.0,v in weight1| w+v) as w1, "
                f"    reduce(w=0.0,v in weight2| w+v) as w2 "
                f"RETURN "
                f"    personIdsInPath, "
                f"    (w1+w2) as pathWeight "
                f"ORDER BY pathWeight desc",
                database_="neo4j", routing_=RoutingControl.READ,
            )
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            sum_time += total_time
    print(f"Query 14: {sum_time} ms")
    benchmark_total_time += sum_time

    print(f"Total benchmark time: {benchmark_total_time} ms")

    if i != 0:
        avg_bench += benchmark_total_time

print(f"Average benchmark time: {avg_bench/5} ms")
