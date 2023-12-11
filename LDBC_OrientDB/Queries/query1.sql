MATCH 
  {class:person, as:p, where:(p_personid= @personId)} -knows-> {as:person, maxdepth:3, where:(p_firstname = @firstName AND $matched.p <> $currentMatch), pathAlias:pPath},
 {as:p} -has_p_placeid-> {as:place},
 {as:p} -person_university- {as:university}
RETURN
  person.p_personid as friendId,
  person.p_lastname as frientLastName,
  pPath.size() as distanceFromPerson,
  person.p_birthdate as friendBirthDay,
  person.p_creationdate as friendCreationDate,
  person.p_gender as friendGender,
  person.p_browserused as friendBrowserUsed,
  person.p_locationip as friendLocationIp,
  place.pl_name as friendCityName,
    p.both("person_university"):{
    o_name, both("has_o_placeid").pl_name as city
  } as friendUniversities,
  p.both("person_company"):{
    o_name, both("has_o_placeid").pl_name as city
  } as friendCompanies
ORDER BY distanceFromPerson, frientLastName, friendId 
