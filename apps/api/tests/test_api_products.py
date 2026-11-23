URL = "https://www.shop.test/mouse"


def add(client, **data):
    return client.post("/api/products", json={"url": URL, **data})


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_add_and_list_products(client):
    response = add(client, target_price="49.90")

    assert response.status_code == 201
    product = response.json()
    assert (product["store"], product["target_price"]) == ("shop.test", 49.9)
    assert product["created_at"].endswith("Z")
    assert [p["id"] for p in client.get("/api/products").json()] == [product["id"]]


def test_add_same_url_twice(client):
    add(client)

    assert add(client).status_code == 409


def test_add_with_bad_data(client):
    assert client.post("/api/products", json={"url": "not a url"}).status_code == 422
    assert add(client, target_price=-5).status_code == 422


def test_update_only_sent_fields(client):
    product_id = add(client, target_price="10").json()["id"]

    response = client.patch(f"/api/products/{product_id}", json={"alerts_enabled": False})

    assert response.json()["alerts_enabled"] is False
    assert response.json()["target_price"] == 10.0


def test_remove_target_with_null(client):
    product_id = add(client, target_price="10").json()["id"]

    response = client.patch(f"/api/products/{product_id}", json={"target_price": None})

    assert response.json()["target_price"] is None


def test_delete_product(client):
    product_id = add(client).json()["id"]

    assert client.delete(f"/api/products/{product_id}").status_code == 204
    assert client.get(f"/api/products/{product_id}").status_code == 404
    assert client.delete(f"/api/products/{product_id}").status_code == 404
