from planner.containers import create_container


def test_encode_password() -> None:
    
    container = create_container()
    encoder = container.hash_password()
    password = "random-password"
    hashed_password = encoder.create_hash(password)

    assert password != hashed_password

def test_decode_password() -> None:

    container = create_container()
    encoder = container.hash_password()
    password = "random-password"
    hashed_password = encoder.create_hash(password)
    assert encoder.verify_hash(password, hashed_password)