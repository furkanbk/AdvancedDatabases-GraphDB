SELECT 
	friend.p_personid AS personId,
    friend.p_firstname AS personFirstName,
    friend.p_lastname AS personLastName,
    tag.t_name AS tagNames,
    count(distinct(comment)) AS replyCount
FROM(
  MATCH 
	{class:Person, as:person, where:(p_personid = @personId)} -knows-> {as: friend} <-has_m_creatorid- {as: comment}-has_m_c_replyof-> {as:post} -message_tag-> {as:tag} -has_t_tagclassid-> {as:tagClass}
RETURN
    friend,tag,comment,post,tagClass)
WHERE tagClass.tc_name = @tagClassName
GROUP BY friend,tag
ORDER BY
    replyCount DESC,
    personId ASC
LIMIT 20