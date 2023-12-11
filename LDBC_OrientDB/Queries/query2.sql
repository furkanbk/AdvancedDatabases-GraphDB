MATCH
 {class:person, as:p, where:(p_personid = @personId)} -knows-> {as:person},
 {as:person} <-has_m_creatorid- {as:message, where:( date(m_creationdate, 'yyyy-MM-dd HH:mm:ss') <= date(@maxDate, 'yyyy-MM-dd HH:mm:ss') )}
 RETURN 
  person.p_personid as personId,
  person.p_firstname as personFirstName,
  person.p_lastname as personLastName,  
  message.m_messageid as postOrCommentId,
  message.m_content + message.m_ps_imagefile as postOrCommentContent,
  date(message.m_creationdate, 'yyyy-MM-dd HH:mm:ss') as postOrCommentCreationDate
ORDER BY message.creationDate DESC, postOrCommentId ASC
