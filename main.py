from pawpal_system import Task, Pet, Owner, Schedule

# Create an owner
jordan = Owner(name="Jordan", available_minutes=60)

# Create two pets
mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", duration=25, priority="high"))
mochi.add_task(Task(title="Brush fur", duration=15, priority="low"))

# Add tasks to Whiskers
whiskers.add_task(Task(title="Feed breakfast", duration=10, priority="high"))
whiskers.add_task(Task(title="Clean litter box", duration=10, priority="medium"))
whiskers.add_task(Task(title="Play with feather toy", duration=20, priority="low"))

# Add pets to owner
jordan.add_pet(mochi)
jordan.add_pet(whiskers)

# Print all pets and their tasks
print("=== Pets & Tasks ===")
for pet in jordan.pets:
    print(f"\n{pet}")
    for task in pet.tasks:
        print(f"  - {task}")

# Generate and print the schedule
print("\n=== Today's Schedule ===\n")
schedule = Schedule(owner=jordan, date="2026-03-31")
schedule.generate(jordan.get_all_tasks(), jordan.available_minutes)
print(schedule.get_explanation())
