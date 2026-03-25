from modulename.web import server

def test_api_get():
  response = server.test_client().get("/api/hello?name=xtof")
  assert response.status_code == 200
  assert response.data == b'"Hello xtof from REST/GET"\n'

def test_api_post():
  response = server.test_client().post(
    "/api/hello",
    json={"name": "xtof"}
  )
  assert response.status_code == 200
  assert response.data == b'"Hello xtof from REST/POST"\n'
