sample_input = [
    {"country": "FR", "city": "Paris", "currency": "EUR", "amount": 20},
    {"country": "FR", "city": "Lyon", "currency": "EUR", "amount": 11.4},
    {"country": "ES", "city": "Madrid", "currency": "EUR", "amount": 8.9},
    {"country": "US", "city": "Boston", "currency": "USD", "amount": 100},
    {"country": "UK", "city": "London", "currency": "GBP", "amount": 12.2},
    {"country": "UK", "city": "London", "currency": "FBP", "amount": 10.9},
]

sample_output = {
    "EUR": {"ES": {"Madrid": [{"amount": 8.9}]}, "FR": {"Lyon": [{"amount": 11.4}], "Paris": [{"amount": 20}]}},
    "FBP": {"UK": {"London": [{"amount": 10.9}]}},
    "GBP": {"UK": {"London": [{"amount": 12.2}]}},
    "USD": {"US": {"Boston": [{"amount": 100}]}},
}

sample_output_2 = {
    "Boston": [{"amount": 100, "country": "US", "currency": "USD"}],
    "London": [
        {"amount": 12.2, "country": "UK", "currency": "GBP"},
        {"amount": 10.9, "country": "UK", "currency": "FBP"},
    ],
    "Lyon": [{"amount": 11.4, "country": "FR", "currency": "EUR"}],
    "Madrid": [{"amount": 8.9, "country": "ES", "currency": "EUR"}],
    "Paris": [{"amount": 20, "country": "FR", "currency": "EUR"}],
}

sample_output_3 = {
    8.9: {"EUR": [{"city": "Madrid", "country": "ES"}]},
    10.9: {"FBP": [{"city": "London", "country": "UK"}]},
    11.4: {"EUR": [{"city": "Lyon", "country": "FR"}]},
    12.2: {"GBP": [{"city": "London", "country": "UK"}]},
    20: {"EUR": [{"city": "Paris", "country": "FR"}]},
    100: {"USD": [{"city": "Boston", "country": "US"}]},
}

request_data = {
    "json_data": [
        {"country": "US", "city": "New York", "currency": "USD", "amount": 200},
        {"country": "FR", "city": "Paris", "currency": "EUR", "amount": 20},
        {"country": "FR", "city": "Lyon", "currency": "EUR", "amount": 11.4},
        {"country": "ES", "city": "Madrid", "currency": "EUR", "amount": 8.9},
        {"country": "US", "city": "Boston", "currency": "USD", "amount": 100},
        {"country": "UK", "city": "London", "currency": "GBP", "amount": 12.2},
        {"country": "UK", "city": "London", "currency": "FBP", "amount": 10.9},
    ],
    "keys_priority": ["country", "city"],
}

response_data = {
    "result": {
        "errors": "None",
        "payload": {
            "ES": {"Madrid": [{"amount": 8.9, "currency": "EUR"}]},
            "FR": {"Lyon": [{"amount": 11.4, "currency": "EUR"}], "Paris": [{"amount": 20, "currency": "EUR"}]},
            "UK": {"London": [{"amount": 12.2, "currency": "GBP"}, {"amount": 10.9, "currency": "FBP"}]},
            "US": {
                "Boston": [{"amount": 100, "currency": "USD"}],
                "New York": [{"amount": 200, "currency": "USD"}],
            },
        },
    },
    "status": 200,
    "success": True,
}
