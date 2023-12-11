SELECT  if(eval("shortestPathLength >= 0 "),shortestPathLength,-1) as shortestPathLength
FROM(
SELECT sum(path.size()) as shortestPathLength FROM (
  SELECT shortestPath($from, $to, null, "knows") AS path 
  LET 
    $from = (SELECT FROM Person WHERE p_personid = @person1Id), 
    $to = (SELECT FROM Person WHERE p_personid = @person2Id)
  UNWIND path))