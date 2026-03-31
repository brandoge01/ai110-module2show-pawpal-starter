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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
