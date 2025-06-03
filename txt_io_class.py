import ast  



class TxtIOClass:
    def __init__(self, file_path="simple_task.txt"):
        self.file_path = file_path
        self.actions_list = []

    def read_tasks(self):
        data = []
        with open(self.file_path, "r") as file:
            for line in file:
                try:
                    entry = ast.literal_eval(line.strip())  # Convert text to list
                    data.append(entry)
                except Exception as e:
                    print(f"Error parsing line: {line} -> {e}")

        # Output
        for entry in data:
            print(entry)

        self.actions_list = data

    def write_tasks(self, data):
        with open(self.file_path, "w") as file:
            for entry in data:
                file.write(str(entry) + "\n")
        print(f"Data written to {self.file_path}")
        
    def append_tasks(self, data):
        with open(self.file_path, "a") as file:
            for entry in data:
                file.write(str(entry) + "\n")
        print(f"Data appended to {self.file_path}")


    def clear_tasks(self):
        with open(self.file_path, "w") as file:
            file.write("")

if __name__ == "__main__":
    txt_io = TxtIOClass(file_path="output.txt")
    
    #txt_io.clear_tasks()
    # Example of writing tasks
    example_data = [[-0.5585109914360047, -0.015166859282791614, 0.20061496707725524, True]]
    txt_io.append_tasks(example_data)
    
    # Read again to verify
    txt_io.read_tasks()

