import tkinter as tk
import requests

class FlaskAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask App GUI")

        # Entry for selecting a file
        self.file_entry_label = tk.Label(root, text="Select a File:")
        self.file_entry_label.pack()
        self.file_entry = tk.Entry(root)
        self.file_entry.pack()

        # Entry for providing a new filename
        self.new_filename_label = tk.Label(root, text="New Filename:")
        self.new_filename_label.pack()
        self.new_filename_entry = tk.Entry(root)
        self.new_filename_entry.pack()

        # Entry for specifying the destination directory
        self.dest_dir_label = tk.Label(root, text="Destination Directory:")
        self.dest_dir_label.pack()
        self.dest_dir_entry = tk.Entry(root)
        self.dest_dir_entry.pack()

        # Entry for specifying width and height
        self.width_label = tk.Label(root, text="Width:")
        self.width_label.pack()
        self.width_entry = tk.Entry(root)
        self.width_entry.pack()

        self.height_label = tk.Label(root, text="Height:")
        self.height_label.pack()
        self.height_entry = tk.Entry(root)
        self.height_entry.pack()

        # Button to trigger the file upload and rename action
        self.upload_button = tk.Button(root, text="Upload and Rename", command=self.upload_and_rename)
        self.upload_button.pack()

        # Result label to display messages
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def upload_and_rename(self):
        file = self.file_entry.get()
        new_filename = self.new_filename_entry.get()
        selected_directory = self.dest_dir_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()

        try:
            # Send the data to your Flask app for processing
            response = requests.post("http://localhost:5200/New_FlaskAppArchitect/upload_file_rename", data={
                "new_filename": new_filename,
                "selected_directory": selected_directory,
                "width": width,
                "height": height
            }, files={"file": (file, open(file, "rb"))})

            # Display the response message
            self.result_label.config(text=response.text)
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlaskAppGUI(root)
    root.mainloop()
