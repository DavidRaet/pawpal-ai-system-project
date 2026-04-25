import streamlit as st
from pawpal_system import (
    Owner, Pet, Task, PetCareService, PrestonAdvisor,
    Species, Priority, Status, Preferences,
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# Initialize singleton service once per session
if "service" not in st.session_state:
    st.session_state.service = PetCareService.get_instance()
service = st.session_state.service

# ── Owner & Pet Setup ─────────────────────────────────────────────────────────
st.header("Owner & Pet")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    reminder_time = st.time_input("Daily reminder time")  # maps to Preferences.reminderTime

st.markdown("#### Pet Details")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
with col3:
    pet_breed = st.text_input("Breed", value="Shiba Inu")
with col4:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])

# Build real backend objects from current form values
preferences = Preferences(reminder_time=str(reminder_time))
pet = Pet(name=pet_name, age=int(pet_age), breed=pet_breed, species=Species(species))
owner = Owner(name=owner_name, preferences=preferences, pets=[pet])

st.divider()

# ── Add Task ──────────────────────────────────────────────────────────────────
st.header("Add Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add task"):
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=Priority(priority),
        pet=pet,
    )
    service.add_task(task)

st.divider()

# ── Task List & Management ────────────────────────────────────────────────────
st.header("Tasks")

if service._tasks:
    if "status_filter" not in st.session_state:
        st.session_state.status_filter = "All"
    if "priority_filter" not in st.session_state:
        st.session_state.priority_filter = "All"

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed", "Skipped"],
            key="status_filter"
        )
    with col2:
        priority_filter = st.selectbox(
            "Filter by priority", ["All", "High", "Medium", "Low"],
            key="priority_filter"
        )

    if status_filter == "All" and priority_filter == "All":
        displayed = service._tasks
    elif status_filter == "All":
        displayed = service.filter_tasks_by_priority(Priority(priority_filter))
    elif priority_filter == "All":
        displayed = service.filter_tasks_by_status(Status(status_filter))
    else:
        by_status = service.filter_tasks_by_status(Status(status_filter))
        displayed = [t for t in by_status if t.priority == Priority(priority_filter)]

    if displayed:
        for i, task in enumerate(displayed):
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.markdown(
                        f"**{task.title}** — {task.duration_minutes} min"
                        f" | Priority: **{task.priority.value}** | Pet: {task.pet.name}"
                    )
                    st.caption(f"Status: {task.status.value}")
                with col2:
                    if task.status != Status.COMPLETED:
                        if st.button("Complete", key=f"complete_{i}"):
                            task.status = Status.COMPLETED
                            st.rerun()
                with col3:  
                    if task.status != Status.SKIPPED:
                        if st.button("Skip", key=f"skip_{i}"):
                            task.status = Status.SKIPPED
                            st.rerun()
    else:
        st.info("No tasks match the current filters.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Schedule ──────────────────────────────────────────────────────────────────
st.header("Schedule")
st.caption("Generates a priority-ordered plan — completed tasks are excluded.")

if st.button("Generate schedule"):
    schedule = service.generate_schedule()
    if schedule.tasks:
        st.success(schedule.description)
        for task in schedule.tasks:
            st.markdown(
                f"- **{task.title}** ({task.duration_minutes} min)"
                f" — {task.priority.value} priority | Status: {task.status.value}"
                f" | Pet: {task.pet.name}"
            )
    else:
        st.info("All tasks are completed — nothing left to schedule!")

st.divider()

# ── PawPal Preston ────────────────────────────────────────────────────────────
st.header("🐾 Ask PawPal Preston")
st.caption("Your AI pet health advisor — dogs & cats only, backed by trusted veterinary sources.")

if "preston_response" not in st.session_state:
    st.session_state.preston_response = ""

question = st.text_area(
    "Ask Preston a question about your pet's health, behavior, or diet:",
    height=80,
    placeholder="e.g. My dog keeps scratching his ears — what could be causing this?",
)

if st.button("Ask Preston"):
    advisor = PrestonAdvisor()
    st.session_state.preston_response = advisor.ask(question, pet)

if st.session_state.preston_response:
    st.info(st.session_state.preston_response)
