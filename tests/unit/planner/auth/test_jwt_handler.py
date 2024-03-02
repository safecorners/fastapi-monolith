from planner.containers import create_container


def test_create_and_verify_access_token() -> None:
    
    container = create_container()
    jwt_handler = container.jwt_handler()
    
    access_token = jwt_handler.create_access_token("test@example.com")

    data = jwt_handler.verify_access_token(access_token)
    
    assert data["username"] == "test@example.com"