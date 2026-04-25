from pawpal_system import Owner, Pet, Preferences, Status, Task, Priority, Species, PetCareService, PrestonAdvisor

def main():
    # Create an owner
    owner = Owner("John Doe", Preferences("08:00"))
    service = PetCareService.get_instance()

    # Create pets
    pet1 = Pet("Buddy", 5, "Golden Retriever", Species.DOG)
    pet2 = Pet("Mittens", 3, "Siamese", Species.CAT)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    # Create tasks for pet1
    service.add_task(Task("Feed Buddy", 30, Priority.MEDIUM, pet1, None, Status.COMPLETED))
    service.add_task(Task("Walk Buddy", 60, Priority.MEDIUM, pet1))
    service.add_task(Task("Vet appointment for Buddy", 45, Priority.HIGH, pet1))

    # Create tasks for pet2
    service.add_task(Task("Feed Mittens", 20, Priority.MEDIUM, pet2))
    service.add_task(Task("Play with Mittens", 40, Priority.LOW, pet2))
    service.add_task(Task("Groom Mittens", 30, Priority.LOW, pet2))

    # Display owner's pets and their tasks
    print(f"Owner: {owner.name}")
    schedule = service.generate_schedule()
    print("\nGenerated Schedule:")
    for task in schedule.tasks:
        print(f"  - {task.title} for {task.pet.name} with a {task.priority.value} priority. This task will take {task.duration_minutes} minutes. The status of this task is {task.status.value}")

    # PawPal Preston demo
    print("\n--- PawPal Preston ---")
    advisor = PrestonAdvisor()

    q1 = "Buddy has been scratching his ears a lot. What could be causing this?"
    print(f"\nQ: {q1}")
    print(f"A: {advisor.ask(q1, pet1)}")

    q2 = "What is a healthy daily diet for an adult cat like Mittens?"
    print(f"\nQ: {q2}")
    print(f"A: {advisor.ask(q2, pet2)}")

main()