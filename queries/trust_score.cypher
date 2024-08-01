MATCH path = (viewer:User {id: "y4euc58gnmxun9wo87gwmanu6kztt9pgw1zz1yp1azp7trrsjamy"})-[:FOLLOWS*1..3]->(user:User)
MATCH (user)-[:AUTHORED]->(p:Post)
WITH p, length(path) as pathLength
WITH p, CASE 
    WHEN pathLength = 1 THEN 1.0
    WHEN pathLength = 2 THEN 0.5
    WHEN pathLength = 3 THEN 0.25
    ELSE 0.125
END as propagatedScore
RETURN p.id, propagatedScore
ORDER BY propagatedScore DESC