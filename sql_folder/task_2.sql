WITH input AS (
    SELECT ts, user_id, currency, amount, NULL AS to_currency, NULL as rate
    from transactions
    union all
    select ts, null as user_id, from_currency as currency, null as amount, to_currency, rate
    from exchange_rates
    where to_currency = 'GBP'
)
select user_id, sum(amount * coalesce(last_rate, 1))
from (
    select user_id, amount, first_value(rate) over (partition by currency, group_number) as last_rate
    from (
             select user_id, amount, rate, currency, sum(case when rate is not null then 1 end) OVER (partition by currency order by ts) as group_number
             from input
         ) as grouped
    ) as t
where user_id is not null
group by user_id;