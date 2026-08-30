from unittest.mock import Mock

import pytest

import app.services.habit_service as service
from app.exceptions import HabitNotFound
from app.schemas.habit import HabitUpdate


def test_create_habit_success(user, existing_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    repo_mock = Mock(return_value=[habit])
    monkeypatch.setattr(service.repo, "add_habit", repo_mock)
    result = service.create_habit(habit, user)
    repo_mock.assert_called_once_with(habit, user.id)
    assert result == [habit]


def test_get_users_list_habits(user, habit_create_factory, monkeypatch):
    habit = habit_create_factory()
    repo_mock = Mock(return_value=habit)
    monkeypatch.setattr(service.repo, "get_all", repo_mock)
    result = service.list_habits(user)
    repo_mock.assert_called_once_with(user.id)
    assert result == habit


def test_get_habit_success(user, existing_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    repo_mock = Mock(return_value=habit)
    monkeypatch.setattr(service.repo, "get_by_id", repo_mock)
    result = service.get_habit(habit.id, user)
    repo_mock.assert_called_once_with(habit.id, user.id)
    assert result == habit


def test_get_habit_not_found(user, existing_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    repo_mock = Mock(return_value=None)
    monkeypatch.setattr(service.repo, "get_by_id", repo_mock)
    with pytest.raises(HabitNotFound):
        service.get_habit(habit.id, user)
    repo_mock.assert_called_once_with(habit.id, user.id)


def test_delete_habit_success(user, existing_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    get_repo_mock = Mock(return_value=habit)
    delete_repo_mock = Mock()
    monkeypatch.setattr(service.repo, "get_by_id", get_repo_mock)
    monkeypatch.setattr(service.repo, "delete_by_id", delete_repo_mock)
    service.delete_habit(habit.id, user)
    get_repo_mock.assert_called_once_with(habit.id, user.id)
    delete_repo_mock.assert_called_once_with(habit.id, habit.owner_id)


def test_delete_habit_not_found(user, existing_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    get_repo_mock = Mock(return_value=None)
    delete_repo_mock = Mock()
    monkeypatch.setattr(service.repo, "get_by_id", get_repo_mock)
    monkeypatch.setattr(service.repo, "delete_by_id", delete_repo_mock)
    with pytest.raises(HabitNotFound):
        service.delete_habit(habit.id, user)
    get_repo_mock.assert_called_once_with(habit.id, user.id)
    delete_repo_mock.assert_not_called()


def test_update_habit_success(user, existing_habit_factory, update_habit_factory, monkeypatch):
    habit = existing_habit_factory()
    update_habit = update_habit_factory(title="updated_title", description="updated_description")
    get_repo_mock = Mock(return_value=habit)
    upd_repo_mock = Mock()
    monkeypatch.setattr(service.repo, "get_by_id", get_repo_mock)
    monkeypatch.setattr(service.repo, "update", upd_repo_mock)
    service.update_habit(habit.id, update_habit, user)
    get_repo_mock.assert_called_once_with(habit.id, user.id)
    upd_repo_mock.assert_called_once_with(habit, user.id)
    assert habit.title == update_habit.title
    assert habit.description == update_habit.description


def test_update_habit_not_found(user, existing_habit_factory, update_habit_factory, monkeypatch):
    existing_habit = existing_habit_factory()
    update_habit = update_habit_factory()
    get_repo_mock = Mock(return_value=None)
    upd_repo_mock = Mock()
    monkeypatch.setattr(service.repo, "get_by_id", get_repo_mock)
    monkeypatch.setattr(service.repo, "update", upd_repo_mock)

    with pytest.raises(HabitNotFound):
        service.update_habit(existing_habit.id, update_habit, user)

    get_repo_mock.assert_called_once_with(existing_habit.id, user.id)
    upd_repo_mock.assert_not_called()


@pytest.mark.parametrize(
    "updated_habit, expected_title, expected_description",
    [
        (
            HabitUpdate(title="updated_title"),
            "updated_title",
            "exist_habit_description",
        ),
        (
            HabitUpdate(description="updated_description"),
            "exist_habit_title",
            "updated_description",
        ),
        (
            HabitUpdate(),
            "exist_habit_title",
            "exist_habit_description",
        ),
    ],
    ids=[
        "update only title",
        "update only description",
        "update none",
    ],
)
def test_update_habit_partial(
    user, existing_habit_factory, updated_habit, expected_title, expected_description, monkeypatch
):
    # Получаем базовую привычку
    existing_habit = existing_habit_factory()
    # Заглушки
    get_repo_mock = Mock(return_value=existing_habit)
    upd_repo_mock = Mock()
    monkeypatch.setattr(service.repo, "get_by_id", get_repo_mock)
    monkeypatch.setattr(service.repo, "update", upd_repo_mock)
    # Вызываем тестируемую функцию
    service.update_habit(existing_habit.id, updated_habit, user)
    # Проверяем вызовы методов с нужными параметрами
    get_repo_mock.assert_called_once_with(existing_habit.id, user.id)
    upd_repo_mock.assert_called_once_with(existing_habit, user.id)
    # Проверяем что логика соответствует
    assert existing_habit.title == expected_title
    assert existing_habit.description == expected_description
