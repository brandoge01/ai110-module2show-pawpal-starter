import streamlit as st
from pawpal_system import Task, Pet, Owner, Schedule
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Scheduler")

with st.expander("ℹ️ About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** is an intelligent pet care scheduler that helps busy owners plan daily tasks 
for their pets. It features:

✨ **Smart Features:**
- **Priority-based scheduling**: Fits as many high-priority tasks as possible within your time budget
- **Time-sorted display**: View tasks in chronological order for easy planning
- **Recurring tasks**: Automatically generate next occurrences for daily/weekly tasks
- **Conflict detection**: Warns when multiple tasks overlap in time
- **Detailed explanations**: Understand why tasks were scheduled or skipped
"""
    )

st.divider()

# Session state initialization
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)
if "current_pet" not in st.session_state:
    st.session_state.current_pet = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

owner = st.session_state.owner

# Owner Configuration
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("👤 Owner name", value=owner.name)
with col2:
    owner.available_minutes = st.number_input(
        "⏱️ Available minutes today", min_value=1, max_value=480, value=owner.available_minutes
    )

st.divider()

# Pet Management
st.subheader("🐶 Pet Management")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add Pet", use_container_width=True):
        existing_names = [p.name for p in owner.pets]
        if pet_name in existing_names:
            st.warning(f"⚠️ {pet_name} is already added.")
        elif pet_name.strip() == "":
            st.warning("⚠️ Enter a pet name.")
        else:
            owner.add_pet(Pet(name=pet_name, species=species))
            st.success(f"✅ Added {pet_name} the {species}!")

if owner.pets:
    st.markdown("**Current Pets:**")
    pet_cols = st.columns(len(owner.pets))
    for i, pet in enumerate(owner.pets):
        with pet_cols[i]:
            st.info(f"🐾 **{pet.name}** ({pet.species})\n{len(pet.tasks)} task(s)")
else:
    st.info("📝 No pets yet. Add one above to get started!")

st.divider()

# Task Management
st.subheader("📋 Task Management")
if owner.pets:
    st.markdown("**Add a new task:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_pet_name = st.selectbox("Pet", [p.name for p in owner.pets], key="task_pet")
    with col2:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col3:
        task_time = st.text_input("Time (HH:MM)", value="08:00", key="task_time")

    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="task_duration")
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_freq")

    col1, col2, col3 = st.columns(3)
    with col1:
        due_date_input = st.date_input("Due date", value=datetime.now(), key="task_due_date")
    with col2:
        st.empty()
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Task", use_container_width=True, key="add_task_btn"):
            selected_pet = next((p for p in owner.pets if p.name == selected_pet_name), None)
            if selected_pet:
                try:
                    # Validate time format
                    hours, minutes = map(int, task_time.split(':'))
                    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                        st.warning("⚠️ Invalid time. Use HH:MM (00:00 - 23:59)")
                    else:
                        new_task = Task(
                            title=task_title,
                            duration=int(duration),
                            priority=priority,
                            time=task_time,
                            frequency=frequency,
                            due_date=due_date_input.strftime("%Y-%m-%d")
                        )
                        selected_pet.add_task(new_task)
                        st.success(f"✅ Added '{task_title}' to {selected_pet_name}!")
                except ValueError:
                    st.warning("⚠️ Invalid time format. Use HH:MM")

    # Display all tasks in a table
    st.markdown("---")
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.markdown("**All Tasks:**")
        task_data = []
        for pet in owner.pets:
            for task in pet.tasks:
                task_data.append({
                    "Pet": pet.name,
                    "Task": task.title,
                    "Duration (min)": task.duration,
                    "Priority": task.priority.upper(),
                    "Time": task.time,
                    "Frequency": task.frequency,
                    "Status": "✅ Done" if task.completed else "⏳ Pending"
                })
        
        st.dataframe(task_data, use_container_width=True, hide_index=True)
    else:
        st.info("📝 No tasks yet. Add one above.")
else:
    st.info("🐾 Add a pet first before adding tasks.")

st.divider()

# Schedule Generation
st.subheader("📅 Generate Schedule")
col_spacer, col_btn, col_spacer2 = st.columns([1, 2, 1])
with col_btn:
    if st.button("🔄 Generate Optimized Schedule", use_container_width=True):
        all_tasks = owner.get_all_tasks()
        if not all_tasks:
            st.warning("⚠️ No tasks to schedule. Add pets and tasks first.")
        else:
            schedule = Schedule(owner=owner, date=datetime.now().strftime("%Y-%m-%d"))
            schedule.generate(all_tasks, owner.available_minutes)
            st.session_state.schedule = schedule
            st.success("✅ Schedule generated!")

# Display Schedule with Smart Features
if st.session_state.schedule:
    schedule = st.session_state.schedule
    
    st.markdown("---")
    st.markdown("## 📊 Schedule Results")
    
    # Conflict Detection
    conflicts = schedule.detect_conflicts()
    if conflicts:
        st.markdown("### ⚠️ Conflicts Detected")
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("✅ No time conflicts detected!")
    
    st.divider()
    
    # Time-Sorted Planned Tasks
    if schedule.planned_tasks:
        st.markdown("### ✅ Scheduled Tasks (Sorted by Time)")
        sorted_tasks = schedule.sort_by_time(schedule.planned_tasks)
        
        schedule_data = []
        cumulative_time = 0
        for i, task in enumerate(sorted_tasks, 1):
            end_hour = int(task.time.split(':')[0]) + task.duration // 60
            end_min = (int(task.time.split(':')[1]) + task.duration % 60) % 60
            schedule_data.append({
                "#": i,
                "Time": task.time,
                "Task": task.title,
                "Duration": f"{task.duration} min",
                "Priority": task.priority.upper(),
                "End Time": f"{end_hour}:{end_min:02d}"
            })
            cumulative_time += task.duration
        
        st.dataframe(schedule_data, use_container_width=True, hide_index=True)
        
        # Time Budget Display
        col1, col2, col3 = st.columns(3)
        with col2:
            st.metric(
                "Time Budget",
                f"{schedule.total_duration()} / {owner.available_minutes} min",
                f"{owner.available_minutes - schedule.total_duration()} min available"
            )
    else:
        st.info("📌 No tasks fit within available time.")
    
    st.divider()
    
    # Skipped Tasks
    if schedule.skipped_tasks:
        st.markdown("### ⏭️ Skipped (Insufficient Time)")
        skipped_data = []
        for task in schedule.skipped_tasks:
            skipped_data.append({
                "Task": task.title,
                "Duration": f"{task.duration} min",
                "Priority": task.priority.upper(),
                "Reason": "Not enough time remaining"
            })
        st.dataframe(skipped_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Full Explanation
    with st.expander("📋 Full Schedule Explanation", expanded=True):
        st.text(schedule.get_explanation())

