from pawpal_system import Task, Pet, Owner


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


def test_complete_recurring_task_creates_new_instance():
    pet = Pet(name="Mochi", species="dog")
    daily_task = Task(title="Morning walk", duration=20, priority="high", frequency="daily")
    pet.add_task(daily_task)
    
    assert len(pet.tasks) == 1
    assert not pet.tasks[0].completed
    
    pet.complete_task("Morning walk")
    
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed  # Original task is completed
    assert not pet.tasks[1].completed  # New task is pending
    assert pet.tasks[0].title == pet.tasks[1].title  # Same title
    assert pet.tasks[0].frequency == pet.tasks[1].frequency  # Same frequency


def test_detect_conflicts_finds_overlapping_tasks():
    from pawpal_system import Schedule
    
    owner = Owner(name="Test Owner")
    
    # Create two pets with overlapping tasks
    pet1 = Pet(name="Dog", species="dog")
    pet1.add_task(Task(title="Walk", duration=30, time="10:00"))  # 10:00-10:30
    
    pet2 = Pet(name="Cat", species="cat") 
    pet2.add_task(Task(title="Play", duration=20, time="10:15"))  # 10:15-10:35 (overlaps with walk)
    
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    schedule = Schedule(owner, "2024-01-01")
    
    conflicts = schedule.detect_conflicts()
    
    assert len(conflicts) == 1
    assert "Cross-pet conflict" in conflicts[0]
    assert "Walk" in conflicts[0] and "Play" in conflicts[0]
