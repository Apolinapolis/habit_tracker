from app.repositories import user_repository as user_repo


def test_get_user_by_username(clean_users):
    username = "test_username"
    user_repo.create_user(username, "hash_test")
    user = user_repo.get_user_by_username(username)
    assert user.username == username

def test_create_user(clean_users):
    username = "test_username"
    password = "create_user_password"
    user = user_repo.create_user(username, password)
    assert user.username == username
    assert user.hashed_password == password
    assert user.id is not None

def test_user_not_exists(clean_users):
    assert user_repo.get_user_by_username("not_exist_user") is None
