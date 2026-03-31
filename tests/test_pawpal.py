from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Morning walk", duration=20, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Feed dinner", duration=10, priority="medium"))
    assert len(pet.tasks) == 2
