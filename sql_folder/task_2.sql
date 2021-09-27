WITH s_input AS (
    SELECT ts, user_id, currency, amount, NULL AS to_currency, NULL AS rate
    FROM transactions
    UNION ALL
    SELECT ts, NULL AS user_id, from_currency AS currency, NULL AS amount, to_currency, rate
    FROM exchange_rates
    WHERE to_currency = 'GBP'
)
SELECT user_id, SUM(amount * COALESCE(last_rate, 1))
FROM (
    SELECT user_id, amount, first_value(rate) over (partition BY currency, group_number) AS last_rate
    FROM (
             SELECT user_id, amount, rate, currency, SUM(CASE WHEN rate IS NOT NULL THEN 1 END) OVER (partition BY currency ORDER BY ts) AS group_number
             FROM s_input
         ) AS grouped
    ) AS t
WHERE user_id IS NOT NULL
GRUOP BY user_id;