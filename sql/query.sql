-- #############
-- 集計用SQL
-- #############
-- 任意の年月を指定するパラメータ
WITH params AS (
    SELECT
        date_trunc('month', %(start_date_param)s::DATE) AS start_date,
        date_trunc('month', %(end_date_param)s::DATE) + INTERVAL '1 month - 1 day' AS end_date
),
date_range AS (
    SELECT generate_series(
        (SELECT start_date FROM params),  -- 月の初日
        (SELECT end_date FROM params),    -- 月の最終日
        '1 day'::INTERVAL
    )::DATE AS date
),
counts AS (
    SELECT
        DATE(update_date) AS date,
        COUNT(CASE
            WHEN category LIKE ANY (ARRAY['%%AA%%', '%%BB%%'])
                THEN 1
        END) AS all_comment,
        COUNT(CASE
            WHEN category LIKE ANY (ARRAY['%%AA%%', '%%BB%%'])
                AND comment ~ '^(?!.*\*\*).*\*.*$'
                THEN 1
        END) AS mt_comment,
        COUNT(CASE
            WHEN category LIKE ANY (ARRAY['%%AA%%', '%%BB%%'])
                AND (comment ~ '\*\*')
                THEN 1
        END) AS ai_comment
    FROM
        comment
    WHERE
        is_active = TRUE
        AND update_date::DATE BETWEEN (SELECT start_date FROM params) AND (SELECT end_date FROM params)
    GROUP BY
        DATE(update_date)
)
SELECT
    d.date,
    COALESCE(c.all_comment, 0) AS all_comment,
    COALESCE(c.mt_comment, 0) AS mt_comment,
    CASE
        WHEN COALESCE(c.all_comment, 0) > 0
            THEN (COALESCE(c.mt_comment, 0) * 100.0 / COALESCE(c.all_comment, 0))
        ELSE 0
    END AS mt_comment_per,
    COALESCE(c.ai_comment, 0) AS ai_comment,
    CASE
        WHEN COALESCE(c.all_comment, 0) > 0
            THEN (COALESCE(c.ai_comment, 0) * 100.0 / COALESCE(c.all_comment, 0))
        ELSE 0
    END AS ai_comment_per
FROM
    date_range d
LEFT JOIN
    counts c
ON
    d.date = c.date
ORDER BY
    d.date;