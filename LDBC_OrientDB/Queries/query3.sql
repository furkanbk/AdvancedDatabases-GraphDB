SELECT *
FROM(
  MATCH
   {class:Person, as:p, where:(p_personid = @personId)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath}
  RETURN 
    person.p_personid as personId, 
    person.p_firstname as personFirstName, 
    person.p_lastname as personLastName,   
    person.in("has_m_creatorid")[
      date(m_creationdate, 'yyyy-MM-dd HH:mm:ss') >= date(@startDate, 'yyyy-MM-dd HH:mm:ss')
      AND m_creationdate < m_creationdate + 1000*60*60*24 * @durationDays
      AND out("has_m_locationid").pl_name CONTAINS @countryXName
    ].size() as xCount,
 	 person.in("has_m_creatorid")[
      date(m_creationdate, 'yyyy-MM-dd HH:mm:ss') >= date(@startDate, 'yyyy-MM-dd HH:mm:ss')
      AND m_creationdate < m_creationdate + 1000*60*60*24 * @durationDays
      AND out("has_m_locationid").pl_name CONTAINS @countryYName
    ].size() as yCount
    )
WHERE xCount > 0 AND yCount > 0
ORDER BY xCount DESC, personId ASC
