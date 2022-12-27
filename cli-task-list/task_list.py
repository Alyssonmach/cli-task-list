import datetime
import sqlite3
import sys

def is_valid_date(date_string):
    """
    Verifies if a date string in the format 'YYYY-MM-DD' is a valid date.
    
    Parameters:
    date_string (str): The date string to be verified.
    
    Returns:
    bool: True if the date string is valid, False otherwise.
    """

    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def add_task(description, deadline):
    """
    Adds a new task to the database.
    
    Parameters:
    description (str): The description of the task.
    deadline (str): The deadline of the task in the format 'YYYY-MM-DD'.
    
    Returns:
    None
    """

    # Validate inputs
    if not description or not deadline:
        print("Error: Task description and deadline must be provided")
        return

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Add the task to the database
    if is_valid_date(deadline):
        try:
            c.execute("INSERT INTO tasks (description, deadline, completed) VALUES (?, ?, 0)", (description, deadline))
            conn.commit()
            print("Task added successfully")
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
    else:
        print("Invalid date. Please enter a date in the format YYYY-MM-DD")

    # Close the connection to the database
    conn.close()

def view_tasks():
    """
    Shows all tasks in the database.
    
    Parameters:
    None
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Get all tasks from the database
    try:
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        conn.close()
        return

    # Print the tasks
    if tasks:
        print("ID\tDescription\tDeadline\tCompleted")
        for task in tasks:
            completed = "Yes" if task[3] else "No"
            print(f"{task[0]}\t{task[1]}\t{task[2]}\t{completed}")
    else:
        print("No tasks found")

    # Close the connection to the database
    conn.close()

def view_completed_tasks():
    """
    Shows all completed tasks in the database.
    
    Parameters:
    None
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Get all completed tasks from the database
    try:
        c.execute("SELECT * FROM tasks WHERE completed=1")
        tasks = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        conn.close()
        return

    # Print the tasks
    if tasks:
        print("ID\tDescription\tDeadline\tCompleted")
        for task in tasks:
            completed = "Yes" if task[3] else "No"
            print(f"{task[0]}\t{task[1]}\t{task[2]}\t{completed}")
    else:
        print("No completed tasks found")

    # Close the connection to the database
    conn.close()

def view_uncompleted_tasks():
    """
    Shows all uncompleted tasks in the database.
    
    Parameters:
    None
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Get all uncompleted tasks from the database
    try:
        c.execute("SELECT * FROM tasks WHERE completed=0")
        tasks = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        conn.close()
        return

    # Print the tasks
    if tasks:
        print("ID\tDescription\tDeadline\tCompleted")
        for task in tasks:
            completed = "Yes" if task[3] else "No"
            print(f"{task[0]}\t{task[1]}\t{task[2]}\t{completed}")
    else:
        print("No uncompleted tasks found")

    # Close the connection to the database
    conn.close()

def mark_as_completed(task_id, state = True):
    """
    Marks a task as completed in the database.
    
    Parameters:
    task_id (int): The ID of the task to be marked as completed.
    state (bool): The boolean true or false state of the completed activity.
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Mark the task as completed
    if state:
        try:
            c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
            conn.commit()
            print("Task marked as completed successfully")
        except sqlite3.Error as e:
            print(f"Error marking task as completed: {e}")
    else:
        try:
            c.execute("UPDATE tasks SET completed=0 WHERE id=?", (task_id,))
            conn.commit()
            print("Task marked as incompleted successfully")
        except sqlite3.Error as e:
            print(f"Error marking task as incompleted: {e}")

    # Close the connection to the database
    conn.close()

def delete_task(task_id):
    """
    Deletes a task from the database.
    
    Parameters:
    task_id (int): The ID of the task to be deleted.
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Delete the task
    try:
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        print("Task deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")

    # Close the connection to the database
    conn.close()

def view_overdue_tasks():
    """
    Shows all overdue tasks in the database.
    
    Parameters:
    None
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Get all overdue tasks from the database
    try:
        c.execute("SELECT * FROM tasks WHERE completed=0 AND deadline<?", (datetime.datetime.now().strftime('%Y-%m-%d'),))
        tasks = c.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        conn.close()
        return

    # Print the tasks
    if tasks:
        print("ID\tDescription\tDeadline\tCompleted")
        for task in tasks:
            completed = "Yes" if task[3] else "No"
            print(f"{task[0]}\t{task[1]}\t{task[2]}\t{completed}")
    else:
        print("No overdue tasks found")

    # Close the connection to the database
    conn.close()

def view_group_tasks(group_id):
    # terminar essa função
    pass

def update_task_description(task_id, new_description):
    """
    Updates the description of a task in the database.
    
    Parameters:
    task_id (int): The ID of the task to be updated.
    new_description (str): The new description of the task.
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Update the task description
    try:
        c.execute("UPDATE tasks SET description=? WHERE id=?", (new_description, task_id))
        conn.commit()
        print("Task description updated successfully")
    except sqlite3.Error as e:
        print(f"Error updating task description: {e}")

    # Close the connection to the database
    conn.close()

def update_task_deadline(task_id, new_deadline):
    """
    Updates the deadline of a task in the database.
    
    Parameters:
    task_id (int): The ID of the task to be updated.
    new_deadline (str): The new deadline of the task, in the format 'YYYY-MM-DD'.
    
    Returns:
    None
    """

    # Connect to the database
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Update the task deadline
    try:
        c.execute("UPDATE tasks SET deadline=? WHERE id=?", (new_deadline, task_id))
        conn.commit()
        print("Task deadline updated successfully")
    except sqlite3.Error as e:
        print(f"Error updating task deadline: {e}")

    # Close the connection to the database
    conn.close()

def print_tasks(tasks):
    """Print the tasks in a formatted way"""

    for task in tasks:
        print(f"{task[0]}) {task[1]} | Deadline: {task[2]} | Completed: {task[3]}")

def main():
    # Connect to the database
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    # Create the tasks and groups tables if they don't exist
    c.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, description TEXT, deadline DATE, completed INTEGER, group_id INTEGER)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY, name TEXT)"
    )

    # Welcome message
    print("Welcome to the Task Manager!")
    print("Enter a command or type 'help' to see the available commands.")

    while True:

        command = input("> ").split('|')
        command = [s.strip() for s in command]

        # Help command
        if command[0] == "help":
            print("add task | description | deadline | group -> Add a new task")
            print("view tasks -> View all tasks")
            print("view completed -> View completed tasks")
            print("view uncompleted -> View uncompleted tasks")
            print("mark as completed | task_id -> Mark a task as completed")
            print("mark as uncompleted | task_id -> Mark a task as uncompleted")
            print("delete task | task_id -> Delete a task")
            print("view overdue -> View overdue tasks")
            print("update description | task_id | new_description -> Update the description of a task")
            print("update deadline | task_id | new_deadline -> Update the deadline of a task")
            print("exit - Close the application")

        # Add task command
        elif command[0] == "add task":
            # Check if the required number of arguments was provided
            if len(command) != 4:
                print("Error: Invalid number of arguments")
            else:
                # Check if the deadline is in a valid format
                if is_valid_date(command[2]):
                    add_task_to_group(command[1], command[2], command[3])
                    print("Task added!")
                else:
                    print("Error: Invalid date format. Use YYYY-MM-DD")

        # View tasks command
        elif command[0] == "view tasks":
            view_tasks()

        # View completed tasks command
        elif command[0] == "view completed":
            view_completed_tasks()

        # View uncompleted tasks command
        elif command[0] == "view uncompleted":
            view_uncompleted_tasks()

        # Mark as completed command
        elif command[0] == "mark as completed":
            # Check if the required number of arguments was provided
            if len(command) != 2:
                print("Error: Invalid number of arguments")
            else:
                # Check if the task ID is valid
                try:
                    task_id = int(command[1])
                except ValueError:
                    print("Error: Invalid task ID")
                else:
                    mark_as_completed(task_id, stete = True)
                    print("Task marked as completed!")
        
        # Mark as uncompleted command
        elif command[0] == "mark as uncompleted":
            # Check if the required number of arguments was provided
            if len(command) != 2:
                print("Error: Invalid number of arguments")
            else:
                # Check if the task ID is valid
                try:
                    task_id = int(command[1])
                except ValueError:
                    print("Error: Invalid task ID")
                else:
                    mark_as_completed(task_id, state = False)
                    print("Task marked as uncompleted!")

        # Delete task command
        elif command[0] == "delete task":
            # Check if the required number of arguments was provided
            if len(command) != 2:
                print("Error: Invalid number of arguments")
            else:
                # Check if the task ID is valid
                try:
                    task_id = int(command[1])
                except ValueError:
                    print("Error: Invalid task ID")
                else:
                    delete_task(task_id)
                    print("Task deleted!")

        # View overdue tasks command
        elif command[0] == "view overdue":
            view_overdue_tasks()
        
        # Update task description command
        elif command[0] == "update description":
            # Check if the required number of arguments was provided
            if len(command) != 3:
                print("Error: Invalid number of arguments")
            else:
                # Check if the task ID is valid
                try:
                    task_id = int(command[1])
                except ValueError:
                    print("Error: Invalid task ID")
                else:
                    update_task_description(task_id, command[2])
                    print("Task description updated!")

        # Update task deadline command
        elif command[0] == "update deadline":
            # Check if the required number of arguments was provided
            if len(command) != 3:
                print("Error: Invalid number of arguments")
            else:
                # Check if the task ID is valid
                try:
                    task_id = int(command[1])
                except ValueError:
                    print("Error: Invalid task ID")
                else:
                    # Check if the deadline is in a valid format
                    if is_valid_date(command[2]):
                        update_task_deadline(task_id, command[2])
                        print("Task deadline updated!")
                    else:
                        print("Error: Invalid date format. Use YYYY-MM-DD")

        # Exit command
        elif command[0] == "exit":
            # Close the connection to the database
            conn.close()
            # End the program
            sys.exit()

        else:
            print("Error: Invalid command")

if __name__ == "__main__":
    main()
