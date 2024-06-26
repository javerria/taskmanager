from objects import Task, AdminUser


def create_task(app):
    """Prompt the user to enter a task title and description, 
    create a new Task object, and save it to the file.
    
    """
    task_title = input("Please enter a title: ")
    task_description = input("Please enter a description: ")
    new_task = Task(task_title, task_description)
    write_task_to_file(app, new_task)
    print("Task created successfully!")


def write_task_to_file(app, task):
    """Write a single task to the tasks file.

    """
    with open(app.all_tasks_file, "a") as file:
        file.write(
            f"{task.task_name},{task.task_description},{1 if task.task_is_complete else 0}\n"
        )


def edit_task(app):
    """Prompt the user to select a task and enter a new description,
    then update the task description in the file.

    """
    view_all_tasks(app)
    index = (
        int(input("Enter the serial number of the task you would like to edit: ")) - 1
    )
    if is_valid_task_index(app, index):
        new_description = input("Enter new description: ")
        update_task_in_file(app, index, new_description)
        print("Task description updated successfully!")
    else:
        print("Invalid task number.")


def update_task_in_file(app, index, new_description):
    """Update the description of a specific task in the file.

    """
    tasks = read_all_tasks(app)
    if tasks:
        tasks[index].task_description = new_description
        write_tasks_to_file(app, tasks)


def update_task_status(app):
    """Toggle the completion status of a selected task and update the file.

    """
    view_all_tasks(app)
    index = (
        int(
            input(
                "Enter the serial number of the task you want to update the status for: "
            )
        )
        - 1
    )
    if is_valid_task_index(app, index):
        tasks = read_all_tasks(app)
        if tasks:
            tasks[index].task_is_complete = not tasks[index].task_is_complete
            write_tasks_to_file(app, tasks)
            task_status = "complete" if tasks[index].task_is_complete else "incomplete"
            print(f"Task '{tasks[index].task_name}' status updated to {task_status}.")
    else:
        print("Invalid task number.")


def view_all_tasks(app):
    """Display all tasks with their current statuses.

    """
    tasks = read_all_tasks(app)
    if not tasks:
        print("No tasks available.")
    else:
        print("Current tasks:\n")
        for index, task in enumerate(tasks):
            print(
                f"{index + 1}. {task.task_name} - {task.task_description} ({'complete' if task.task_is_complete else 'incomplete'})"
            )


def read_all_tasks(app):
    """Read all tasks from the tasks file and return them as a list of Task objects.

    """
    tasks = []
    try:
        with open(app.all_tasks_file, "r") as file:
            for line in file:
                task_data = line.strip().split(",")
                if (
                    len(task_data) == 3
                ):  # Ensure correct format: name, description, is_complete
                    tasks.append(
                        Task(task_data[0], task_data[1], bool(int(task_data[2])))
                    )
    except FileNotFoundError:
        print("File not found.")
    return tasks


def is_valid_task_index(app, index):
    """Check if the given index is valid for the list of tasks.

    """
    tasks = read_all_tasks(app)
    return 0 <= index < len(tasks)


def write_tasks_to_file(app, tasks):
    """Write the list of tasks to the tasks file, overwriting existing content.

    """
    with open(app.all_tasks_file, "w") as file:
        for task in tasks:
            file.write(
                f"{task.task_name},{task.task_description},{1 if task.task_is_complete else 0}\n"
            )


def assign_task(app):
    """Assign a task to an employee by email. Only admin users can assign tasks.

    """
    if not isinstance(app.current_user, AdminUser):
        print("Only admin users can assign tasks.")
        return
    view_all_tasks(app)
    index = int(input("Enter the serial number of the task you want to assign: ")) - 1
    if is_valid_task_index(app, index):
        tasks = read_all_tasks(app)
        if tasks:
            task = tasks[index]
            assignee_email = input(
                "Enter the email address of the employee you want to assign it to: "
            )
            print(f"Task '{task.task_name}' assigned to {assignee_email}.")
        else:
            print("No tasks available.")
    else:
        print("Invalid task number.")


def delete_task(app):
    """Delete a task from the list. Only admin users can delete tasks.
    
    """
    if not isinstance(app.current_user, AdminUser):
        print("Only admin users can delete tasks.")
        return
    view_all_tasks(app)
    index = (
        int(input("Enter the serial number of the task you would like to delete: ")) - 1
    )
    if is_valid_task_index(app, index):
        tasks = read_all_tasks(app)
        if tasks:
            removed_task = tasks.pop(index)
            write_tasks_to_file(app, tasks)
            print(f"Task '{removed_task.task_name}' has been deleted.")
    else:
        print("Invalid task number.")
