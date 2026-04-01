# PawPal+ Project Reflection

## 1. System Design

Three core actions:
1. Add a Pet - Registers a pet (include name and species) so the system knows who needs care
2. Add a Care Task - Create individual tasks like walking, feeding, or grooming (include duration and priority)
3. Generate a Daily Schedule - Produce an optimized daily plan that can complete as many tasks as possible into available time (prioritize based on priority)

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Task - Represents a single care activity. Holds a title, duration in minutes, priority level (high/medium/low), and completion status. Responsible for tracking its own state (marking itself complete) and converting its priority to a numeric value for sorting.
Pet - Represents an individual pet. Stores the pet's name, species, and a list of Task objects. Responsible for managing its own task list (adding, removing, and filtering tasks by priority).
Owner - Represents the pet owner. Holds the owner's name, available time budget in minutes, and a list of Pet objects. Responsible for managing pets and aggregating all tasks across every pet into a single list for scheduling.
Schedule - The "brain" of the system. Takes an owner and a date, then generates an optimized daily plan. Sorts all tasks by priority (highest first), greedily fills the time budget, and separates tasks into planned vs. skipped lists. Also responsible for producing a human-readable explanation of the schedule and the reasoning behind what was included or excluded.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

No, I didn't make any design changes during the implementation as I was brainstorming with Copilot extensively before implementing any features. Most of the bottlenecks were pretty minor problems or would be relatively complex to implement (e.g. changing the scheduling from greedy to another sorting algorithm)
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two main constraints: time budget (the owner's total available minutes) and task priority (high, medium, or low). It sorts tasks by priority first, then fills the time budget from the top down. Time was the hard constraint since you physically cannot exceed available minutes, while priority determined the order because ensuring critical care tasks happen before optional ones reflects how real pet owners make decisions under time pressure.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a greedy algorithm that sorts tasks by priority (high to low) and schedules them in that order until the available time budget is exhausted. This approach prioritizes getting the most important tasks done first, but doesn't always produce the most optimal schedule that maximizes the total number of completed tasks.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to execute simple coding tasks, brainstorm plans togeher, and to give me explanation for code/algorithims.
Most of the debugging was done through reading the code but AI provided good explanations. I tried to keep my prompts or questions straightforward and one task at a time.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I was asking the AI for the mermaid diagram and skeleton of the program, I didn't like certain design decisions for modularity, so I changed it to be more readable. I evaluate and verify AI suggestions with the Co-pilot feature that shows all the changes with before and afters. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

We tested that the recurring tasks worked, tasks were sorted in a greedy manner, sorting was done time-based, there was time conflict detection, task management, and schedule reasoning. These tests were all important because they are the core logical functionalities of the program. The tests proved the baseline implementation worked and the user wouldn't have a faulty program. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

4.5/5
I would try to stress test the program more by adding more tasks and a lot of overlapping tasks with different time prioritiesm durations, and weights. This way I can see the program works no matter how busy the schedule gets. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm satisifed with the planning and execution of the framework for this project. I thought the UI and logic came out pretty well after thorough planning with Co-pilot.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the UI to be more clean and intuitive. There isn't much user feedback throughout the software so users can get a bit confused easily. Logicly, I think the program is good besides just using the naive greedy sorting algorithm. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Working with AI requires a lot of context building and explanations like talking to an actual human. Extensive planning in your own head has to be exchanged with the AI promptly to bounce ideas and create the architecture. Building good architecture first also makes the AI generate code very easilly and more accurately. The UI for these software programs need more guidance and specific feedback for improvements. 