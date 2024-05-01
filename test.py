import tkinter as tk

class LoginFrame(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Login!")

  def init_components(self):
    self.frame = tk.Frame(self)
    self.frame.pack(padx=10, pady=10)  # Add padding around frame

    self.login_button = tk.Button(self.frame, text="Login", command=self.login_action)
    self.login_button.pack(fill=tk.BOTH, expand=True)  # Fill and expand frame

    self.exit_button = tk.Button(self.frame, text="Exit", command=self.quit)
    self.exit_button.pack(fill=tk.X, expand=True)  # Fill horizontally, expand

  def login_action(self):
    print("Login button clicked!")  # Replace with your desired login action

  def run(self):
    self.init_components()
    self.mainloop()

if __name__ == "__main__":
  test = LoginFrame()
  test.run()
