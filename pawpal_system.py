from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration: int
    priority: str = "medium"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def priority_value(self) -> int:
        """Return numeric priority: high=3, medium=2, low=1."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 0)

    def __str__(self) -> str:
        status = "Done" if self.completed else "Pending"
        return f"{self.title} ({self.duration}min, {self.priority} priority) [{status}]"


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str):
        """Remove a task by its title."""
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_tasks_by_priority(self, priority: str) -> list:
        """Return all tasks matching the given priority level."""
        return [t for t in self.tasks if t.priority == priority]

    def __str__(self) -> str:
        return f"{self.name} ({self.species}) - {len(self.tasks)} task(s)"


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list:
        """Collect all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Schedule:
    def __init__(self, owner: Owner, date: str):
        self.owner = owner
        self.date = date
        self.planned_tasks: list = []
        self.skipped_tasks: list = []

    def generate(self, tasks: list, available_minutes: int):
        """Build an optimized schedule sorted by priority, fitting within the time budget."""
        self.planned_tasks = []
        self.skipped_tasks = []

        sorted_tasks = sorted(tasks, key=lambda t: t.priority_value(), reverse=True)

        remaining_minutes = available_minutes
        for task in sorted_tasks:
            if task.duration <= remaining_minutes:
                self.planned_tasks.append(task)
                remaining_minutes -= task.duration
            else:
                self.skipped_tasks.append(task)

    def total_duration(self) -> int:
        """Return the sum of durations for all planned tasks."""
        return sum(task.duration for task in self.planned_tasks)

    def get_explanation(self) -> str:
        """Return a string explaining why tasks were ordered, included, or skipped."""
        lines = [f"Schedule for {self.owner.name} on {self.date}"]
        lines.append(f"Time budget: {self.owner.available_minutes} minutes\n")

        if self.planned_tasks:
            lines.append("Planned tasks (highest priority first):")
            for i, task in enumerate(self.planned_tasks, 1):
                lines.append(f"  {i}. {task}")
            lines.append(f"\nTotal scheduled: {self.total_duration()} minutes")
        else:
            lines.append("No tasks could be scheduled.")

        if self.skipped_tasks:
            lines.append("\nSkipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"  - {task}")

        return "\n".join(lines)
