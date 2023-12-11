MATCH 
  {class:Person, as:person, where:(p_personid = @personId)}<-has_m_creatorid-{as:message}<-has_m_c_replyof-{as:comment}-has_m_creatorid->{as:commentAuthor}
RETURN
	commentAuthor.p_personid AS personId,
    commentAuthor.p_firstname AS personFirstName,
    commentAuthor.p_lastname AS personLastName,
    comment.m_creationdate AS commentCreationDate,
    comment.m_messageid AS commentId,
    comment.m_content AS commentContent
ORDER BY
    commentCreationDate DESC,
    commentId ASC
LIMIT 20