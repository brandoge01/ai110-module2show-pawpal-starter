```mermaid
classDiagram
    direction LR

    class Owner {
        -String name
        -int available_minutes
        -List~Pet~ pets
        +add_pet(pet: Pet) void
        +remove_pet(pet_name: String) void
        +get_all_tasks() List~Task~
    }

    class Pet {
        -String name
        -String species
        -List~Task~ tasks
        +add_task(task: Task) void
        +remove_task(task_title: String) void
        +get_tasks_by_priority(priority: String) List~Task~
    }

    class Task {
        -String title
        -int duration
        -String priority
        -bool completed
        +mark_complete() void
        +priority_value() int
    }

    class Schedule {
        -Owner owner
        -String date
        -List~Task~ planned_tasks
        -List~Task~ skipped_tasks
        +generate(tasks: List~Task~, available_minutes: int) void
        +total_duration() int
        +get_explanation() String
    }

    Owner "1" --> "*" Pet : has
    Pet "1" --> "*" Task : has
    Schedule "1" --> "1" Owner : belongs to
    Schedule "1" --> "*" Task : plans/skips
```
