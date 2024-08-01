MATCH (u:User)-[rel:BOOKMARKED|REPLIED|REPOSTED|TAGGED]->(p:Post)
        RETURN u.id AS user_id, p.id AS post_id, type(rel) AS interaction_type