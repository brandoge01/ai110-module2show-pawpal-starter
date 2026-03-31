from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str
    duration: int
    priority: str = "medium"
    completed: bool = False
    time: str = "00:00"
    frequency: str = "once"  # "once", "daily", "weekly"
    due_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def priority_value(self) -> int:
        """Return numeric priority: high=3, medium=2, low=1."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 0)

    def __str__(self) -> str:
        status = "Done" if self.completed else "Pending"
        freq_info = f", {self.frequency}" if self.frequency != "once" else ""
        return f"{self.title} ({self.duration}min, {self.priority} priority, {self.time}{freq_info}) [{status}]"


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

    def complete_task(self, task_title: str):
        """Mark a task as completed and automatically create the next recurrence.
        
        For recurring tasks (daily or weekly), this method automatically generates
        a new task instance for the next occurrence and adds it to the pet's task list.
        Uses timedelta for accurate date calculations.
        
        Args:
            task_title (str): The title of the task to mark as completed.
        
        Returns:
            None. Modifies the task in place and adds a new task if recurring.
        
        Behavior:
            - Daily tasks: New task due_date = today + 1 day
            - Weekly tasks: New task due_date = today + 7 days
            - One-time tasks: Only marked complete, no new task created
        """
        for task in self.tasks:
            if task.title == task_title and not task.completed:
                task.mark_complete()
                
                # Create next occurrence for recurring tasks
                if task.frequency == "daily":
                    next_date = datetime.strptime(task.due_date, "%Y-%m-%d") + timedelta(days=1)
                    new_task = Task(
                        title=task.title,
                        duration=task.duration,
                        priority=task.priority,
                        time=task.time,
                        frequency=task.frequency,
                        due_date=next_date.strftime("%Y-%m-%d")
                    )
                    self.add_task(new_task)
                elif task.frequency == "weekly":
                    next_date = datetime.strptime(task.due_date, "%Y-%m-%d") + timedelta(weeks=1)
                    new_task = Task(
                        title=task.title,
                        duration=task.duration,
                        priority=task.priority,
                        time=task.time,
                        frequency=task.frequency,
                        due_date=next_date.strftime("%Y-%m-%d")
                    )
                    self.add_task(new_task)
                break

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

    def filter_tasks(self, completed=None, pet_name=None) -> list:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            completed: If True, return only completed tasks. If False, only incomplete. If None, ignore.
            pet_name: If provided, return only tasks for that pet. If None, ignore.
        
        Returns:
            List of filtered tasks.
        """
        filtered_tasks = []
        for pet in self.pets:
            if pet_name is None or pet.name == pet_name:
                for task in pet.tasks:
                    if completed is None or task.completed == completed:
                        filtered_tasks.append(task)
        return filtered_tasks


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

    def sort_by_time(self, tasks: list) -> list:
        """Sort tasks chronologically by their scheduled time.
        
        Converts HH:MM time strings to minutes since midnight for accurate sorting.
        Uses a lambda function as the sort key to handle time format conversion.
        
        Args:
            tasks (list): List of Task objects to sort.
        
        Returns:
            list: Tasks sorted in chronological order (earliest first).
            
        Example:
            Tasks at 08:00, 20:00, 15:00 → sorted to 08:00, 15:00, 20:00
        """
        return sorted(tasks, key=lambda t: int(t.time.split(':')[0]) * 60 + int(t.time.split(':')[1]))

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

    def detect_conflicts(self) -> list:
        """Detect and report time conflicts between all pending tasks.
        
        Scans all pets' pending (incomplete) tasks and identifies any time overlaps.
        Uses a lightweight warning strategy that returns messages rather than throwing
        exceptions, making the system robust and user-friendly.
        
        Returns:
            list: Warning messages for each conflict found. Empty list if no conflicts.
        
        Conflict Types:
            - Same-pet conflict: Two tasks for the same pet overlap in time.
            - Cross-pet conflict: Tasks from different pets overlap in time.
        
        Algorithm:
            - Complexity: O(n²) where n = number of pending tasks
            - Compares all task pairs and checks if time ranges overlap
            - Uses formula: max(start_a, start_b) < min(end_a, end_b)
        """
        warnings = []
        
        # Get all pending tasks from all pets
        all_pending_tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.completed:
                    all_pending_tasks.append((task, pet.name))
        
        # Convert tasks to include timing information
        task_info = []
        for task, pet_name in all_pending_tasks:
            start_minutes = int(task.time.split(':')[0]) * 60 + int(task.time.split(':')[1])
            end_minutes = start_minutes + task.duration
            task_info.append({
                'task': task,
                'pet': pet_name,
                'start_minutes': start_minutes,
                'end_minutes': end_minutes
            })
        
        # Check for conflicts between all pairs of tasks
        for i in range(len(task_info)):
            for j in range(i + 1, len(task_info)):
                task_a = task_info[i]
                task_b = task_info[j]
                
                # Check if time ranges overlap
                if max(task_a['start_minutes'], task_b['start_minutes']) < min(task_a['end_minutes'], task_b['end_minutes']):
                    if task_a['pet'] == task_b['pet']:
                        warnings.append(f"WARNING: Same-pet conflict - '{task_a['task'].title}' and '{task_b['task'].title}' for {task_a['pet']} overlap in time!")
                    else:
                        warnings.append(f"WARNING: Cross-pet conflict - '{task_a['task'].title}' ({task_a['pet']}) and '{task_b['task'].title}' ({task_b['pet']}) overlap in time!")
        
        return warnings
