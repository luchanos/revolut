async def test_make_nested_json(test_cli):
    resp = await test_cli.post('/make_nested_json')
    assert resp.status_code == 401
    resp_json = resp.json()
    assert resp_json == {'errors': ['No token!'], 'success': False}
