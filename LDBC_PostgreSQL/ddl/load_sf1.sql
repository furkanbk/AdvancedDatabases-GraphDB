-- Populate forum table
copy forum FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/forum_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_person table
copy forum_person FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/forum_hasMember_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_tag table
copy forum_tag FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/forum_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate organisation table
copy organisation FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/static/organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person table
copy person FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_email table
copy person_email FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_email_emailaddress_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_tag table
copy person_tag FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_hasInterest_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate knows table
copy knows ( k_person1id, k_person2id, k_creationdate) FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;
copy knows ( k_person2id, k_person1id, k_creationdate) FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate likes table
copy likes FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_likes_post_0_0.csv' WITH DELIMITER '|' CSV HEADER;
copy likes FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_likes_comment_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_language table
copy person_language FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_speaks_language_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_university table
copy person_university FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_studyAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_company table
copy person_company FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/person_workAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate place table
copy place FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/static/place_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate message_tag table
copy message_tag FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/post_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;
copy message_tag FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/comment_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tagclass table
copy tagclass FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/static/tagclass_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tag table
copy tag FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/static/tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

CREATE TABLE country AS
    SELECT city.pl_placeid AS ctry_city, ctry.pl_name AS ctry_name
    FROM place city, place ctry
    WHERE city.pl_containerplaceid = ctry.pl_placeid
      AND ctry.pl_type = 'country';

-- Populate posts and comments tables, union them into message
copy post FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/post_0_0.csv' WITH DELIMITER '|' CSV HEADER;
copy comment FROM 'D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/social_network-csv_merge_foreign-sf1/dynamic/comment_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Note: to distinguish between "post" and "comment" records:
--   - m_c_replyof IS NULL for all "post" records
--   - m_c_replyof IS NOT NULL for all "comment" records
CREATE TABLE message AS
    SELECT m_messageid, m_ps_imagefile, m_creationdate, m_locationip, m_browserused, m_ps_language, m_content, m_length, m_creatorid, m_locationid, m_ps_forumid, NULL AS m_c_replyof
    FROM post
    UNION ALL
    SELECT m_messageid, NULL, m_creationdate, m_locationip, m_browserused, NULL, m_content, m_length, m_creatorid, m_locationid, NULl, coalesce(m_replyof_post, m_replyof_comment)
    FROM comment;

DROP TABLE post;
DROP TABLE comment;