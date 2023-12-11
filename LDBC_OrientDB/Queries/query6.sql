SELECT tagName, COUNT(*) as postCount
FROM(
MATCH  
		{class:Person, as:p, where:(p_personid = @personId)} -knows-> {as:person, maxdepth:1, where:($matched.p <> $currentMatch), pathAlias:pPath},
      {as:person}<-has_m_creatorid-{as:post}-message_tag->{as:otherTag, where: (t_name= @tagName)},
  {as:post}-message_tag->{as:otherTag2, where: (t_name<> @tagName)}
RETURN otherTag2.t_name as tagName)
GROUP BY tagName
ORDER BY
    postCount DESC,
    tagName ASC
LIMIT 10