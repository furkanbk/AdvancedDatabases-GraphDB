SELECT
	liker.p_personid AS personId,
    liker.p_firstname AS personFirstName,
    liker.p_lastname AS personLastName,
    latestTime AS likeCreationDate,
    message.m_messageid AS commentOrPostId,
    message.m_content + message.m_ps_imagefile AS commentOrPostContent,
     (date(latestTime, 'yyyy-MM-dd HH:mm:ss') -
    date(message.m_creationdate, 'yyyy-MM-dd HH:mm:ss')) as Latency
FROM(
SELECT message,liker,person,min(likeTime) as latestTime, friend
FROM
(SELECT message, liker, person, message.oute('likes').l_creationdate AS likeTime, friend
FROM(
MATCH 
  {class:Person, as:person, where:(p_personid = @personId)}<-has_m_creatorid-{as:message}.(outE("likes").inV()){as:liker},
  {as:person}-knows->{as:friend}
RETURN liker,person,message,friend)
)
GROUP BY message,liker,person
)
ORDER BY
    likeCreationDate DESC,
    personId ASC
LIMIT 20