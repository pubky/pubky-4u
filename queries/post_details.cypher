MATCH (p:Post)
OPTIONAL MATCH (p)<-[rel:TAGGED]-(u:User)
OPTIONAL MATCH (author:User)-[:AUTHORED]->(p)
RETURN p.id AS post_id, p.content AS content, p.indexed_at AS indexed_at,
       COLLECT(u.id) AS tagged_users, COUNT(rel) AS tag_count,
       author.id AS user_id
