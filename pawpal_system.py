from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration: int
    priority: str = "medium"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        pass

    def priority_value(self) -> int:
        """Return numeric priority: high=3, medium=2, low=1."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task for this pet."""
        pass

    def remove_task(self, task_title: str):
        """Remove a task by its title."""
        pass

    def get_tasks_by_priority(self, priority: str) -> list:
        """Return all tasks matching the given priority level."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        pass

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        pass

    def get_all_tasks(self) -> list:
        """Collect all tasks across all pets."""
        pass


class Schedule:
    def __init__(self, owner: Owner, date: str):
        self.owner = owner
        self.date = date
        self.planned_tasks: list = []
        self.skipped_tasks: list = []

    def generate(self, tasks: list, available_minutes: int):
        """Build an optimized schedule sorted by priority, fitting within the time budget."""
        pass

    def total_duration(self) -> int:
        """Return the sum of durations for all planned tasks."""
        pass

    def get_explanation(self) -> str:
        """Return a string explaining why tasks were ordered, included, or skipped."""
        pass
