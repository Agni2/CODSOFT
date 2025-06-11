class TaskBox:
    def __init__(self):
        self.items = []
        self.next = 1

    def add(self, text):
        task = {"id": self.next, "description": text, "completed": False}
        self.items.append(task)
        self.next += 1
        print(f"Added: '{text}' (#{task['id']})")

    def show(self):
        if not self.items:
            print("Nothing to do.")
            return

        print("\nTo-Dos:")
        for x in self.items:
            mark = "✔" if x["completed"] else " "
            print(f"{x['id']}. [{mark}] {x['description']}")
        print()

    def done(self, task_id):
        for x in self.items:
            if x["id"] == task_id:
                if x["completed"]:
                    print(f"#{task_id} already done.")
                else:
                    x["completed"] = True
                    print(f"Done: #{task_id}")
                return
        print(f"ID {task_id} not found.")

    def drop(self, task_id):
        for i, x in enumerate(self.items):
            if x["id"] == task_id:
                self.items.pop(i)
                print(f"Dropped: #{task_id}")
                return
        print(f"No task with ID {task_id}.")

def run():
    box = TaskBox()
    print("To-Do CLI (add/show/done/drop/quit)")

    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "quit":
            break
        elif cmd == "add":
            t = input("Task? ").strip()
            if t:
                box.add(t)
        elif cmd == "show":
            box.show()
        elif cmd == "done":
            try:
                box.done(int(input("ID? ")))
            except:
                print("Invalid ID.")
        elif cmd == "drop":
            try:
                box.drop(int(input("ID? ")))
            except:
                print("Invalid ID.")
        else:
            print("Try add/show/done/drop/quit")

if __name__ == "__main__":
    run()
