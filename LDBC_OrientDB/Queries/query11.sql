SELECT
		otherPerson.p_personid AS personId,
        otherPerson.p_firstname AS personFirstName,
        otherPerson.p_lastname AS personLastName,
        company.o_name AS organizationName,
        startYear
FROM(
SELECT person, country.pl_name, otherPerson, min(otherPerson.inE('person_company').pc_workfrom) as startYear
FROM(
MATCH 
	 {class:Person, as:person, where:(p_personid = @personId)}-knows-{as:otherPerson, maxdepth:2, where:($matched.person <> $currentMatch), pathAlias:pPath},
     {as:otherPerson}-person_company-{as: company}-has_o_placeid->{as: country}
RETURN
       person, otherPerson,country)
       
WHERE country.pl_name = @countryName
group by person,country,otherPerson)
WHERE startYear <= workFromYear

ORDER BY
        startYear ASC,
        personId ASC,
        organizationName DESC
LIMIT 10