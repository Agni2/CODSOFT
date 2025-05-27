import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x400")
        self.root.resizable(True, True)  
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)

        self.data_file = "todo_gui.json"
        self.task_list = []
        self._load_from_file()
        
        self._setup_ui()
        self.refresh_display()

    def _setup_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_row = ttk.Frame(container)
        top_row.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_row, text="New Task:").pack(side=tk.LEFT)

        self.input_field = ttk.Entry(top_row, width=40)
        self.input_field.pack(side=tk.LEFT, padx=5)
        self.input_field.bind("<Return>", lambda e: self._add_item())

        submit_btn = ttk.Button(top_row, text="Add Task", command=self._add_item)
        submit_btn.pack(side=tk.LEFT)

        # Main list area
        task_box = ttk.Frame(container)
        task_box.pack(fill=tk.BOTH, expand=True)

        # Task Table
        self.tree = ttk.Treeview(
            task_box,
            columns=('id', 'description', 'created', 'status'),
            show='headings',
            selectmode='browse'
        )

        self.tree.heading('id', text='ID')
        self.tree.heading('description', text='Description')
        self.tree.heading('created', text='Created')
        self.tree.heading('status', text='Status')

        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('description', width=220, anchor=tk.W)
        self.tree.column('created', width=150, anchor=tk.W)
        self.tree.column('status', width=100, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(task_box, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons for actions
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(10, 0))

        mark_done_btn = ttk.Button(actions, text="Mark Complete", command=self.mark_task_done)
        mark_done_btn.pack(side=tk.LEFT, padx=5)

        del_btn = ttk.Button(actions, text="Delete Task", command=self.remove_task)
        del_btn.pack(side=tk.LEFT, padx=5)

        wipe_btn = ttk.Button(actions, text="Clear All", command=self.wipe_all)
        wipe_btn.pack(side=tk.LEFT, padx=5)

    def _load_from_file(self):
        if os.path.isfile(self.data_file):
            with open(self.data_file, 'r') as file:
                self.task_list = json.load(file)
        else:
            self.task_list = []

    def _save_to_file(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.task_list, f, indent=4)

    def _add_item(self):
        text = self.input_field.get().strip()
        if not text:
            messagebox.showwarning("Hold up", "Please enter something for the task.")
            return

        new_task = {
            'id': len(self.task_list) + 1,  
            'description': text,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'completed': False
        }

        self.task_list.append(new_task)
        self._save_to_file()
        self.refresh_display()
        self.input_field.delete(0, tk.END)
        messagebox.showinfo("Task Added", "Alright, your task was added.")

    def refresh_display(self):
        # Wipe old items from view
        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in self.task_list:
            state = "Completed" if task.get('completed') else "Pending"
            self.tree.insert('', tk.END, values=(
                task['id'],
                task['description'],
                task['created'],
                state
            ))

    def mark_task_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Oops", "Please select a task to complete.")
            return

        item = self.tree.item(selected[0])
        selected_id = item['values'][0]

        for task in self.task_list:
            if task['id'] == selected_id:
                if task.get('completed'):
                    messagebox.showinfo("Already Done", "Looks like this task is already marked complete.")
                    return
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_to_file()
                self.refresh_display()
                messagebox.showinfo("Success", "Task marked as completed.")
                return

        messagebox.showerror("Error", "Hmm, couldn't find the task to mark.")

    def remove_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Choose a task to delete.")
            return

        item = self.tree.item(selected[0])
        target_id = item['values'][0]

        if messagebox.askyesno("Confirm", "Delete this task?"):
            for idx, task in enumerate(self.task_list):
                if task['id'] == target_id:
                    del self.task_list[idx]
                    self._save_to_file()
                    self.refresh_display()
                    messagebox.showinfo("Deleted", "Task was removed.")
                    return

            messagebox.showerror("Error", "Something went wrong. Task not found.")

    def wipe_all(self):
        if not self.task_list:
            messagebox.showinfo("Nothing Here", "No tasks to clear.")
            return

        if messagebox.askyesno("Confirm", "Clear everything?"):
            self.task_list = []
            self._save_to_file()
            self.refresh_display()
            messagebox.showinfo("Cleared", "All tasks wiped out.")

# App entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()
