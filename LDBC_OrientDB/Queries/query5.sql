SELECT forum.f_title as forumTitle, Count(*) as postCount
FROM(
MATCH
   {class:Person, as:p, where:(p_personid = @personId)} -knows-> {as:person, maxdepth:1, where:($matched.p <> $currentMatch), pathAlias:pPath},
    {as:person}.(inE("forum_person"){where: (date(fp_joindate, 'yyyy-MM-dd HH:mm:ss') >= date(@minDate, 'yyyy-MM-dd HH:mm:ss'))}.bothV()){as:forum} <-has_m_ps_forumid- {as:post}
  RETURN 
  	forum,post)
GROUP BY forum
ORDER BY
    postCount DESC,
    forum.f_forumid ASC
LIMIT 20