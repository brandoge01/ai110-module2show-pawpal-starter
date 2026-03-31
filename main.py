from pawpal_system import Task, Pet, Owner, Schedule

# Create an owner
jordan = Owner(name="Jordan", available_minutes=60)

# Create two pets
mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

# Add tasks to Mochi (out of time order)
mochi.add_task(Task(title="Evening brush", duration=15, priority="low", time="20:00"))
mochi.add_task(Task(title="Morning walk", duration=25, priority="high", time="08:00", frequency="daily"))
mochi.add_task(Task(title="Afternoon walk", duration=20, priority="medium", time="15:00", completed=True))
mochi.add_task(Task(title="Quick evening walk", duration=10, priority="medium", time="18:15"))  # Overlaps with Whiskers' play time (18:00-18:20)

# Add tasks to Whiskers (out of time order)
whiskers.add_task(Task(title="Play with feather toy", duration=20, priority="low", time="18:00"))  # 18:00-18:20
whiskers.add_task(Task(title="Feed breakfast", duration=10, priority="high", time="07:00", frequency="daily"))
whiskers.add_task(Task(title="Clean litter box", duration=10, priority="medium", time="12:00", frequency="weekly"))
whiskers.add_task(Task(title="Evening feed", duration=5, priority="high", time="19:00"))
whiskers.add_task(Task(title="Morning grooming", duration=15, priority="medium", time="07:30"))  # Overlaps with Mochi's morning walk

# Add pets to owner
jordan.add_pet(mochi)
jordan.add_pet(whiskers)

# Print all pets and their tasks
print("=== Pets & Tasks ===")
for pet in jordan.pets:
    print(f"\n{pet}")
    for task in pet.tasks:
        print(f"  - {task}")

# Demonstrate sorting by time
print("\n=== Tasks Sorted by Time ===")
schedule = Schedule(owner=jordan, date="2026-03-31")
all_tasks = jordan.get_all_tasks()
sorted_tasks = schedule.sort_by_time(all_tasks)
for task in sorted_tasks:
    print(f"  - {task}")

# Demonstrate filtering by completion status
print("\n=== Completed Tasks Only ===")
completed_tasks = jordan.filter_tasks(completed=True)
for task in completed_tasks:
    print(f"  - {task}")

print("\n=== Incomplete Tasks Only ===")
incomplete_tasks = jordan.filter_tasks(completed=False)
for task in incomplete_tasks:
    print(f"  - {task}")

# Demonstrate filtering by pet name
print("\n=== Tasks for Mochi Only ===")
mochi_tasks = jordan.filter_tasks(pet_name="Mochi")
for task in mochi_tasks:
    print(f"  - {task}")

print("\n=== Tasks for Whiskers Only ===")
whiskers_tasks = jordan.filter_tasks(pet_name="Whiskers")
for task in whiskers_tasks:
    print(f"  - {task}")

# Demonstrate combined filtering
print("\n=== Incomplete Tasks for Whiskers ===")
whiskers_incomplete = jordan.filter_tasks(completed=False, pet_name="Whiskers")
for task in whiskers_incomplete:
    print(f"  - {task}")

# Demonstrate recurring task completion
print("\n=== Demonstrating Recurring Tasks ===")
print("Before completing daily tasks:")
all_tasks_before = jordan.get_all_tasks()
for task in all_tasks_before:
    if "daily" in str(task):
        print(f"  - {task}")

print("\nCompleting 'Morning walk' (daily task)...")
mochi.complete_task("Morning walk")

print("\nCompleting 'Feed breakfast' (daily task)...")
whiskers.complete_task("Feed breakfast")

print("\nAfter completing daily tasks (new instances created):")
all_tasks_after = jordan.get_all_tasks()
for task in all_tasks_after:
    if "daily" in str(task):
        print(f"  - {task}")

print("\nCompleting 'Clean litter box' (weekly task)...")
whiskers.complete_task("Clean litter box")

print("\nAfter completing weekly task (new instance created):")
weekly_tasks = [t for t in jordan.get_all_tasks() if "weekly" in str(t)]
for task in weekly_tasks:
    print(f"  - {task}")

# Generate and print the schedule
print("\n=== Today's Schedule ===\n")
schedule = Schedule(owner=jordan, date="2026-03-31")
schedule.generate(jordan.get_all_tasks(), jordan.available_minutes)
print(schedule.get_explanation())

# Check for conflicts
print("\n=== Conflict Detection ===")
conflicts = schedule.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No time conflicts detected in the schedule.")
