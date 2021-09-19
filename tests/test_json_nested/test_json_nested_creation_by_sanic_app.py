from copy import deepcopy

from tests.test_json_nested.data_for_testing import request_data, response_data


async def test_make_nested_json(test_cli):
    resp = await test_cli.post("/make_nested_json", json=request_data, headers={"X-TOKEN": "test_token"})
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["status"] == response_data["status"]
    assert resp_json["success"] is response_data["success"]
    assert resp_json["result"] == response_data["result"]


async def test_make_nested_json_without_auth(test_cli):
    resp = await test_cli.post("/make_nested_json")
    assert resp.status_code == 401
    resp_json = resp.json()
    assert resp_json == {"errors": ["No token!"], "success": False}


async def test_make_nested_json_wrong_keys_number(test_cli):
    corrupted_request_data = deepcopy(request_data)
    corrupted_request_data["json_data"][0].pop("city")
    resp = await test_cli.post("/make_nested_json", json=corrupted_request_data, headers={"X-TOKEN": "test_token"})
    assert resp.status_code == 422
    resp_json = resp.json()
    assert resp_json == {
        "result": {
            "errors": "{'json_data': ['Keys in different dictionaries must be " "the same!']}",
            "payload": {},
        },
        "status": 422,
        "success": False,
    }


async def test_make_nested_json_no_keys_priority(test_cli):
    corrupted_request_data = deepcopy(request_data)
    corrupted_request_data.pop("keys_priority")
    resp = await test_cli.post("/make_nested_json", json=corrupted_request_data, headers={"X-TOKEN": "test_token"})
    assert resp.status_code == 422
    resp_json = resp.json()
    assert resp_json == {
        "result": {"errors": "{'keys_priority': ['Missing data for required field.']}", "payload": {}},
        "status": 422,
        "success": False,
    }


async def test_make_nested_json_empty_keys_priority(test_cli):
    corrupted_request_data = deepcopy(request_data)
    corrupted_request_data["keys_priority"] = []
    resp = await test_cli.post("/make_nested_json", json=corrupted_request_data, headers={"X-TOKEN": "test_token"})
    assert resp.status_code == 422
    resp_json = resp.json()
    assert resp_json == {
        "result": {
            "errors": "{'keys_priority': ['keys_priority field cannot be empty " "for that method!']}",
            "payload": {},
        },
        "status": 422,
        "success": False,
    }
