SELECT 
  (SELECT tag, COUNT(*) as invalid
   FROM (
     MATCH 
       {class:person, as:p, where:(p_personid = @personId)}-knows->{as:friend},
       {as:friend}<-forum_person-{as:post}-forum_tag->{as:tag}
     RETURN post,tag
   )
   WHERE date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') <= date(@startDate, 'yyyy-MM-dd HH:mm:ss')
   GROUP BY tag
   LIMIT 10) AS invalid,

  (SELECT tag, COUNT(*) as valid
   FROM (
     MATCH 
       {class:person, as:p, where:(p_personid = @personId)}-knows->{as:friend},
       {as:friend}<-forum_person-{as:post}-forum_tag->{as:tag}
     RETURN post,tag
   )
   WHERE date(@startDate, 'yyyy-MM-dd HH:mm:ss') <= date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') AND date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') < date(@startDate +  1000*60*60*24 * @durationDays,'yyyy-MM-dd HH:mm:ss')
   GROUP BY tag
   LIMIT 10) AS valid;

