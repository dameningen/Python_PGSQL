-- #############
-- 集計用SQL
-- #############
WITH counts AS ( 
  SELECT
      DATE (update_date) AS date
      , COUNT( 
          CASE 
              WHEN category like any (array [['%%AA%%', '%%BB%%'] ]) 
                  THEN 1 
              END
      ) AS all_comment
      , COUNT( 
          CASE 
              WHEN category like any (array [['%%AA%%', '%%BB%%'] ]) 
              AND comment ~ '^(?!.*\*\*).*\*.*$' 
                  THEN 1 
              END
      ) AS mt_comment
      , COUNT( 
          CASE 
              WHEN category like any (array [['%%AA%%', '%%BB%%'] ]) 
              AND (comment ~ '\*\*') 
                  THEN 1 
              END
      ) AS ai_comment 
  FROM
      comment
  WHERE
      is_active = TRUE
  GROUP BY
      DATE (update_date)
) 
SELECT
  date
  , all_comment
  , mt_comment
  , CASE 
      WHEN all_comment > 0 
          THEN ( 
          mt_comment * 100.0 / all_comment
      ) 
      ELSE 0 
      END AS mt_comment_per
  , ai_comment
  , CASE 
      WHEN all_comment > 0 
          THEN ( 
          ai_comment * 100.0 / all_comment
      ) 
      ELSE 0 
      END AS ai_comment_per 
FROM
  counts 
ORDER BY
  date;