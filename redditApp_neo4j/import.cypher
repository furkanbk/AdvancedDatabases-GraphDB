LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
MERGE (s:Subreddit {subredditName: row.node})
RETURN count(s);

:auto
LOAD CSV WITH HEADERS FROM 'file:///title_relationships.csv' AS row
CALL{
 WITH row
 MATCH (s1:Subreddit {subredditName: row.SOURCE_SUBREDDIT})
 MATCH (s2:Subreddit {subredditName: row.TARGET_SUBREDDIT})
 CREATE (s1)-[rel:TITLE_HYPERLINK {postID: row.POST_ID, 
									timestamp: datetime(replace(row.TIMESTAMP,' ','T')),
									isNegative: toBoolean(toInteger(row.IS_NEGATIVE)), 
									swear: toFloat(row.LIWC_Swear), anger: toFloat(row.LIWC_Anger), 
									sad: toFloat(row.LIWC_Sad), dissent: toFloat(row.LIWC_Dissent)
 }]->(s2)
} IN TRANSACTIONS OF 500 ROWS;
