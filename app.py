import streamlit as st
from pawpal_system import Task, Pet, Owner, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state — only runs once per session
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

if "schedule" not in st.session_state:
    st.session_state.schedule = None

owner = st.session_state.owner

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available minutes today", min_value=1, max_value=480, value=owner.available_minutes
)
owner.name = owner_name
owner.available_minutes = available_minutes

st.divider()

st.subheader("Add a Pet")
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_pet2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing_names = [p.name for p in owner.pets]
    if pet_name in existing_names:
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    pet_options = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_options)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        new_task = Task(title=task_title, duration=int(duration), priority=priority)
        selected_pet.add_task(new_task)
        st.success(f"Added '{task_title}' to {selected_pet_name}!")

    st.markdown("### Current Tasks")
    for pet in owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}:**")
            for task in pet.tasks:
                st.write(f"  - {task}")
    if not owner.get_all_tasks():
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.warning("No tasks to schedule. Add pets and tasks first.")
    else:
        schedule = Schedule(owner=owner, date="2026-03-31")
        schedule.generate(all_tasks, owner.available_minutes)
        st.session_state.schedule = schedule
        st.success("Schedule generated!")

if st.session_state.schedule:
    st.text(st.session_state.schedule.get_explanation())
