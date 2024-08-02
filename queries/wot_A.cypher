// Network propagation trust score + Post interaction
// TODO: Refactor
MATCH path = shortestPath((viewer:User {id: "y4euc58gnmxun9wo87gwmanu6kztt9pgw1zz1yp1azp7trrsjamy"})-[:FOLLOWS*1..3]->(friendOfFriend:User))
MATCH (friendOfFriend)-[:AUTHORED]->(post:Post)
WHERE NOT (viewer)-[:AUTHORED]->(post)
WITH DISTINCT post, friendOfFriend, length(path) as pathLength

OPTIONAL MATCH (post)<-[replies:REPLIED]-(replyPost:Post)
WITH post, friendOfFriend, pathLength, count(replies) AS repliesCount

OPTIONAL MATCH (post)<-[tagged:TAGGED]-(taggedUser:User)
WITH post, friendOfFriend, pathLength, repliesCount, count(tagged) AS taggedCount

OPTIONAL MATCH (post)<-[reposted:REPOSTED]-(taggedUser:Post)
WITH post, friendOfFriend, pathLength, repliesCount, taggedCount, count(reposted) AS repostCount

OPTIONAL MATCH (post)<-[bookmarked:BOOKMARKED]-(bookmarkUser:User)
WITH post, friendOfFriend, pathLength, repliesCount, taggedCount, repostCount, 
     count(bookmarked) AS bookmarkCount

WITH post, friendOfFriend, repliesCount, taggedCount, repostCount, bookmarkCount,
     CASE 
         WHEN pathLength = 1 THEN 1.0
         WHEN pathLength = 2 THEN 0.5
         WHEN pathLength = 3 THEN 0.25
         ELSE 0.125
     END as propagated

WITH post, friendOfFriend, 
     (repliesCount + taggedCount + repostCount + bookmarkCount) AS engagement,
     propagated

RETURN post.id AS post_id, 
       engagement,
       propagated,
       (engagement * propagated) AS combined,
       friendOfFriend.name as post_owner
ORDER BY combined DESC