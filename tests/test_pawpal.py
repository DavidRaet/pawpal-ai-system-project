"""Pytest suite for pawpal_system.py."""

import pytest
from pawpal_system import (
    Pet, Task, PetCareService, 
    Species, Priority, Status, PrestonAdvisor,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_service():
    """Reset the singleton before and after every test to avoid state bleed."""
    PetCareService._instance = None
    yield
    PetCareService._instance = None


@pytest.fixture
def service():
    return PetCareService.get_instance()


@pytest.fixture
def dog():
    return Pet(name="Buddy", age=5, breed="Golden Retriever", species=Species.DOG)


@pytest.fixture
def cat():
    return Pet(name="Mittens", age=3, breed="Siamese", species=Species.CAT)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_singleton(service):
    """get_instance() must always return the same object."""
    second = PetCareService.get_instance()
    assert service is second


def test_add_and_retrieve_task(service, dog):
    """A task added via add_task should be retrievable via get_tasks_for_pet."""
    task = Task(title="Morning walk", duration_minutes=30, priority=Priority.MEDIUM, pet=dog)
    service.add_task(task)
    tasks = service.get_tasks_for_pet(dog)
    assert task in tasks


def test_remove_task(service, dog):
    """After remove_task, the task should no longer appear for that pet."""
    task = Task(title="Evening walk", duration_minutes=20, priority=Priority.LOW, pet=dog)
    service.add_task(task)
    service.remove_task(task)
    assert task not in service.get_tasks_for_pet(dog)


def test_generate_schedule_sorts_by_priority(service, dog):
    """generate_schedule must return HIGH-priority tasks before LOW-priority ones."""
    low_task = Task(title="Play", duration_minutes=15, priority=Priority.LOW, pet=dog)
    high_task = Task(title="Vet visit", duration_minutes=45, priority=Priority.HIGH, pet=dog)
    service.add_task(low_task)
    service.add_task(high_task)

    schedule = service.generate_schedule()
    titles = [t.title for t in schedule.tasks]
    assert titles.index("Vet visit") < titles.index("Play")


def test_generate_schedule_excludes_completed(service, dog):
    """generate_schedule must not include tasks with Status.COMPLETED."""
    done = Task(title="Feed", duration_minutes=10, priority=Priority.HIGH, pet=dog,
                status=Status.COMPLETED)
    pending = Task(title="Walk", duration_minutes=30, priority=Priority.MEDIUM, pet=dog)
    service.add_task(done)
    service.add_task(pending)

    schedule = service.generate_schedule()
    assert done not in schedule.tasks
    assert pending in schedule.tasks


def test_filter_tasks_by_status(service, dog):
    """filter_tasks_by_status should return only tasks matching the given status."""
    pending = Task(title="Walk", duration_minutes=30, priority=Priority.MEDIUM, pet=dog)
    completed = Task(title="Feed", duration_minutes=10, priority=Priority.HIGH, pet=dog,
                     status=Status.COMPLETED)
    service.add_task(pending)
    service.add_task(completed)

    result = service.filter_tasks_by_status(Status.PENDING)
    assert pending in result
    assert completed not in result


def test_filter_tasks_by_priority(service, dog, cat):
    """filter_tasks_by_priority should return only tasks with the given priority."""
    high = Task(title="Vet visit", duration_minutes=45, priority=Priority.HIGH, pet=dog)
    low = Task(title="Groom", duration_minutes=20, priority=Priority.LOW, pet=cat)
    service.add_task(high)
    service.add_task(low)

    result = service.filter_tasks_by_priority(Priority.HIGH)
    assert high in result
    assert low not in result


def test_get_tasks_for_pet_is_pet_specific(service, dog, cat):
    """get_tasks_for_pet must only return tasks assigned to the requested pet."""
    dog_task = Task(title="Walk", duration_minutes=30, priority=Priority.MEDIUM, pet=dog)
    cat_task = Task(title="Play", duration_minutes=15, priority=Priority.LOW, pet=cat)
    service.add_task(dog_task)
    service.add_task(cat_task)

    assert dog_task in service.get_tasks_for_pet(dog)
    assert cat_task not in service.get_tasks_for_pet(dog)


# ---------------------------------------------------------------------------
# PrestonAdvisor tests
# ---------------------------------------------------------------------------

def test_preston_rejects_empty_question(dog, monkeypatch):
    """Input guardrail: empty question must return a prompt-to-fill message."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    advisor = PrestonAdvisor()
    response = advisor.ask("", dog)
    assert "enter a question" in response.lower()


def test_preston_rejects_other_species(monkeypatch):
    """Input guardrail: Species.OTHER must return a specialist-referral message."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    exotic = Pet("Tweety", 2, "Canary", Species.OTHER)
    advisor = PrestonAdvisor()
    response = advisor.ask("Is my bird eating enough?", exotic)
    assert "specializes in dogs and cats" in response


def test_preston_returns_ai_response_for_valid_question(dog, monkeypatch):
    """Valid dog question must return the Gemini response (mocked to avoid real API call)."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    advisor = PrestonAdvisor()
    monkeypatch.setattr(
        advisor._client,
        "complete",
        lambda s, u: "Per VCA Animal Hospitals, dogs need balanced nutrition.",
    )
    response = advisor.ask("What should I feed my dog?", dog)
    assert len(response) > 20
    assert "VCA" in response
