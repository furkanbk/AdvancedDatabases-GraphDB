SELECT 
	person.p_personid AS personId,
    person.p_firstname AS personFirstName,
    person.p_lastname AS personLastName,
    message.m_messageid AS commentOrPostId,
    message.m_content + message.m_ps_imagefile AS commentOrPostContent,
    message.m_creationdate AS commentOrPostCreationDate
FROM(
MATCH 
	{class:Person, as:p, where:(p_personid = @personId)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath},
	{as:person}<-has_m_creatorid-{as: message}
return person,message)
WHERE date(message.m_creationdate,'yyyy-MM-dd HH:mm:ss') < date(@maxDate, 'yyyy-MM-dd HH:mm:ss')
ORDER BY
    commentOrPostCreationDate DESC,
    message.m_messageid ASC
LIMIT 20