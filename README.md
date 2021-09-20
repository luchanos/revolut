# Revolut
REST-API application for nesting json. Sanic - async web-framework, but this task 
cannot show async domination((

####Created by luchanos:

- t.me/luchanos
- lukash_91@mail.ru
- facebook.com/luchanos
- youtube.com/luchanos
- linkedin.com/in/luchanos

## fuctionalities
This application contains endpoint for nested dictionaries
creation from flat dictionaries.

## dependencies installation
pip3 install -r requirements.txt

## running tests

- For running test first of all please set TEST_MODE = True in enviroment
variables (you can use you IDE configurations or create your own local test settings file)

## linters

- If you modify the codebase of this app, please make command
  
```make linters```

in your terminal for running linters.

Behavior of the linters you can set in isort, flake8, pyproject and Makefile files.

## endpoints

- /make_nested_json [POST]

This endpoint receive POST request with list of flat dictionaries and keys for aggregation and respond with 
nested dictionary.

<i><b>Contracts</i></b>:

{"json_data": [
  {
    "country": str,
    "city": str,
    "currency": str,
    "amount": float
  },
  ...
  ...
  ...
],
"keys_priority": [non empty array of str]
}

An example of request:

curl --location --request POST 'http://<YOUR_SHINY_HOST>:<YOUR_SHINY_PORT>/make_nested_json' \
--header 'X-TOKEN: <YOUR_SHINY_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{"json_data": [
  {
    "country": "US",
    "city": "New York",
    "currency": "USD",
    "amount": 200
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  }
],
"keys_priority": ["country", "city"]
}'```

## auth

- For basic auth you must add 'X-TOKEN' header in your request. An example of token you can find in Dockerfile.
I set it there just to simplify, in real life service tokens is not recommended to keep in codebase - that's
not securable. If someone got an access to your code it may be stolen.

## scripts

- Same task solver script you can find in 'scripts' folder with an example of flat json. For running via terminal use:

```cat flat_json.json | python create_nested_json.py currency country city```

- Just for fun I've created file to send test data to database in async mode by my own client.

## deployment

- You can create an image of your application by using Dockerfile and then create some instances in containers. Dockerfile
contains everything, what you need for that.

- If you don't want to set up Docker container settings you can use docker-compose-local file - here you can find our app
and Postgres (I've just wanna to create other endpoints for writing in database, but my time quota for free coding has
been ended this weekend regretfully :D )
  
# migrations

For run migrations you can use yoyo-migrations lib. All migrations you can find in 'migrations' folder.
Applying for container db from local compose file:

```yoyo apply --database postgresql://postgres:dbpass@localhost:5432/postgres```

# P.S. 
THIS APP HAD BEEN DEPLOYED IN THE WEB!!! :)
So, you can check its functionality by sending some curl to http://84.201.128.178:3000/make_nested_json with 
token from Dockerfile (a1f64cd8-69b9-493c-8587-7afc041efabe)

Thanks for attention!
