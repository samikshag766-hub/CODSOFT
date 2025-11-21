import json
import os

FILE_NAME = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# Display all tasks
def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found!\n")
        return
    print("\nYour To-Do List:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["completed"] else "❌"
        print(f"{i}. {task['title']} [{status}]")
    print()

# Add a new task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    if title:
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        print("Task added successfully!\n")
    else:
        print("Task title cannot be empty!\n")

# Mark task as completed
def complete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task_num = int(input("Enter task number to mark as completed: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed!\n")
        else:
            print("Invalid task number!\n")
    except ValueError:
        print("Please enter a valid number!\n")

# Delete a task
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            deleted = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Deleted task: {deleted['title']}\n")
        else:
            print("Invalid task number!\n")
    except ValueError:
        print("Please enter a valid number!\n")

# Main program loop
def main():
    tasks = load_tasks()
    while True:
        print("===== TO-DO LIST MENU =====")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Exiting To-Do List. Goodbye!!")
            break
        else:
            print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    main()

