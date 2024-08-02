// Post interaction FoF
MATCH (viewer:User {id: "y4euc58gnmxun9wo87gwmanu6kztt9pgw1zz1yp1azp7trrsjamy"})-[:FOLLOWS*2]->(friendOfFriend:User)-[:AUTHORED]->(post:Post)
WHERE NOT (viewer)-[:AUTHORED]->(post)
WITH DISTINCT post, friendOfFriend

OPTIONAL MATCH (post)<-[replies:REPLIED]-(replyPost:Post)
WITH post, count(replies) AS repliesCount, friendOfFriend

OPTIONAL MATCH (post)<-[tagged:TAGGED]-(taggedUser:User)
WITH post, repliesCount, count(tagged) AS taggedCount, friendOfFriend

OPTIONAL MATCH (post)<-[reposted:REPOSTED]-(taggedUser:Post)
WITH post, repliesCount, taggedCount, count(reposted) AS repostCount, friendOfFriend

OPTIONAL MATCH (post)<-[bookmarked:BOOKMARKED]-(bookmarkUser:User)
WITH post, friendOfFriend, repliesCount, taggedCount, repostCount, 
     count(bookmarked) AS bookmarkCount

ORDER BY repliesCount DESC, taggedCount DESC
//LIMIT 10

RETURN post.id AS post_id, (repliesCount + taggedCount +repostCount + bookmarkCount) AS total, friendOfFriend.name as post_owner
ORDER BY total DESC