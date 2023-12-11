SELECT	
	  person.p_personid AS personId,
      person.p_firstname AS personFirstName,
      person.p_lastname AS personLastName,
      total AS commonInterestScore,
      person.p_gender AS personGender,
      city.pl_name AS personCityName
FROM(
SELECT person, post, city, Count(*) as total
FROM(
SELECT person, person.in('has_m_creatorid') as post , person.in('has_m_creatorid').out('message_tag').in('person_tag') as start, city
FROM(
SELECT p, person, city, birthday
FROM(
SELECT p, city, person, person.p_birthday as birthday
FROM(

MATCH 
	{class:Person, as:p, where:(p_personid = @personId)} -knows-> {as:person, maxdepth:1, where:($matched.p <> $currentMatch), pathAlias:pPath},
    {as:person}-has_p_placeid->{as: city}
RETURN 
	p, person, city))
WHERE (birthday.format('MM') = @month AND birthday.format('dd') >= 21 ) OR
		(birthday.format('MM') = @modMonth AND birthday.format('dd') < 22 ))
)
GROUP BY person, post, city
)

GROUP BY friend
ORDER BY commonInterestScore DESC, personId ASC
LIMIT 10 