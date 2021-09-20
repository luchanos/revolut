SELECT sum(amount / orig_rate) AS exchanged_total_result, user_id
FROM (

SELECT
--- adding 1 to GBP
COALESCE(rate, 1) AS orig_rate, user_id, amount
FROM transactions tr

LEFT JOIN (

-- get exchange rates for the last day
SELECT DISTINCT ON (from_currency) from_currency , rate
FROM exchange_rates er
WHERE to_currency = 'GBP'
ORDER BY from_currency , ts desc) ex

ON ex.from_currency = tr.currency) g

GROUP BY user_id;