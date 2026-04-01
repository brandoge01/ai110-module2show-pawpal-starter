from pawpal_system import Task, Pet, Owner, Schedule
from datetime import datetime, timedelta


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
    daily_task = Task(title="Morning walk", duration=20, priority="high", frequency="daily", due_date="2024-01-10")
    pet.add_task(daily_task)
    
    assert len(pet.tasks) == 1
    assert not pet.tasks[0].completed
    
    pet.complete_task("Morning walk")
    
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed  # Original task is completed
    assert not pet.tasks[1].completed  # New task is pending
    assert pet.tasks[0].title == pet.tasks[1].title  # Same title
    assert pet.tasks[0].frequency == pet.tasks[1].frequency  # Same frequency
    
    # Verify the new task is for the following day
    original_date = datetime.strptime(pet.tasks[0].due_date, "%Y-%m-%d")
    new_date = datetime.strptime(pet.tasks[1].due_date, "%Y-%m-%d")
    assert new_date == original_date + timedelta(days=1)  # Next day confirmed


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Mochi", species="dog")
    
    # Add tasks in non-chronological order
    pet.add_task(Task(title="Evening play", duration=30, time="18:00"))
    pet.add_task(Task(title="Morning walk", duration=20, time="08:00"))
    pet.add_task(Task(title="Lunch feed", duration=10, time="12:30"))
    pet.add_task(Task(title="Midnight snack", duration=5, time="23:59"))
    
    owner.add_pet(pet)
    schedule = Schedule(owner, "2024-01-01")
    
    # Sort tasks by time
    sorted_tasks = schedule.sort_by_time(pet.tasks)
    
    # Verify chronological order
    assert sorted_tasks[0].title == "Morning walk"
    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].title == "Lunch feed"
    assert sorted_tasks[1].time == "12:30"
    assert sorted_tasks[2].title == "Evening play"
    assert sorted_tasks[2].time == "18:00"
    assert sorted_tasks[3].title == "Midnight snack"
    assert sorted_tasks[3].time == "23:59"
    
    # Verify all tasks are present
    assert len(sorted_tasks) == 4


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


def test_weekly_task_creates_next_week_occurrence():
    """Verify weekly recurring tasks advance by 7 days, not 1 day."""
    pet = Pet(name="Mochi", species="dog")
    weekly_task = Task(title="Grooming", duration=45, priority="high", frequency="weekly", due_date="2024-01-08")
    pet.add_task(weekly_task)
    
    assert len(pet.tasks) == 1
    pet.complete_task("Grooming")
    
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed
    assert not pet.tasks[1].completed
    
    # Verify the new task is exactly 7 days later
    original_date = datetime.strptime(pet.tasks[0].due_date, "%Y-%m-%d")
    new_date = datetime.strptime(pet.tasks[1].due_date, "%Y-%m-%d")
    assert new_date == original_date + timedelta(weeks=1)


def test_month_boundary_daily_recurrence():
    """Verify daily tasks correctly handle month boundaries (Jan 31 → Feb 1)."""
    pet = Pet(name="Buddy", species="dog")
    daily_task = Task(title="Daily med", duration=5, priority="high", frequency="daily", due_date="2024-01-31")
    pet.add_task(daily_task)
    
    pet.complete_task("Daily med")
    
    assert len(pet.tasks) == 2
    original_date = datetime.strptime(pet.tasks[0].due_date, "%Y-%m-%d")
    new_date = datetime.strptime(pet.tasks[1].due_date, "%Y-%m-%d")
    
    # Should be Feb 1, not wrapping incorrectly
    assert new_date.month == 2
    assert new_date.day == 1
    assert new_date == original_date + timedelta(days=1)


def test_schedule_generation_priority_ordering():
    """Verify schedule respects priority: high > medium > low within time budget."""
    owner = Owner(name="Busy owner", available_minutes=60)
    pet = Pet(name="Max", species="dog")
    
    # Add tasks with different priorities, random order
    pet.add_task(Task(title="Low priority task", duration=30, priority="low", time="10:00"))
    pet.add_task(Task(title="High priority task", duration=25, priority="high", time="11:00"))
    pet.add_task(Task(title="Medium priority task", duration=20, priority="medium", time="12:00"))
    
    owner.add_pet(pet)
    schedule = Schedule(owner, "2024-01-01")
    
    schedule.generate(owner.get_all_tasks(), owner.available_minutes)
    
    # With 60 min budget: high (25) + medium (20) = 45 min, fits. Low (30) would exceed.
    assert len(schedule.planned_tasks) == 2
    assert len(schedule.skipped_tasks) == 1
    
    # Verify high and medium are selected, low is skipped
    planned_titles = [t.title for t in schedule.planned_tasks]
    assert "High priority task" in planned_titles
    assert "Medium priority task" in planned_titles
    assert "Low priority task" not in planned_titles
    assert "Low priority task" in [t.title for t in schedule.skipped_tasks]


def test_same_pet_conflict_detection():
    """Verify conflicts are detected when same pet has overlapping tasks."""
    owner = Owner(name="Test Owner")
    pet = Pet(name="Dog", species="dog")
    
    # Add two overlapping tasks for the same pet
    pet.add_task(Task(title="Walk", duration=30, time="10:00"))  # 10:00-10:30
    pet.add_task(Task(title="Training", duration=20, time="10:20"))  # 10:20-10:40 (overlaps with walk)
    
    owner.add_pet(pet)
    schedule = Schedule(owner, "2024-01-01")
    
    conflicts = schedule.detect_conflicts()
    
    assert len(conflicts) == 1
    assert "Same-pet conflict" in conflicts[0]
    assert "Walk" in conflicts[0] and "Training" in conflicts[0]


def test_no_conflicts_with_non_overlapping_tasks():
    """Verify no conflicts are reported when all tasks fit within their time slots."""
    owner = Owner(name="Test Owner")
    pet = Pet(name="Dog", species="dog")
    
    # Add non-overlapping tasks
    pet.add_task(Task(title="Walk", duration=30, time="08:00"))  # 08:00-08:30
    pet.add_task(Task(title="Feed", duration=10, time="09:00"))  # 09:00-09:10
    pet.add_task(Task(title="Play", duration=20, time="10:00"))  # 10:00-10:20
    
    owner.add_pet(pet)
    schedule = Schedule(owner, "2024-01-01")
    
    conflicts = schedule.detect_conflicts()
    
    assert len(conflicts) == 0
