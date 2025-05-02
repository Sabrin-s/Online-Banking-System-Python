# main.py
import tkinter as tk
from tkinter import messagebox
from backend import BankSystem

bank = BankSystem()
bank.add_customer("Alice", "user1", "pass123")
bank.add_customer("Bob", "user2", "bob456")

class AnimatedPopup(tk.Toplevel):
    def __init__(self, parent, message, success=True):
        super().__init__(parent)
        self.configure(bg="#d1f7c4" if success else "#f7d1d1")
        self.geometry("300x80+600+350")
        self.overrideredirect(True)
        tk.Label(self, text=message, bg=self['bg'], fg="#2f4f4f",
                 font=("Helvetica", 12, "bold")).pack(expand=True)
        self.after(1500, self.destroy)

class BankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🏦 Online Banking System")
        self.master.geometry("420x380")
        self.master.configure(bg="#e6f2ff")
        self.user = None
        self.login_screen()

    def styled_label(self, parent, text, size=12, bold=False):
        font = ("Segoe UI", size, "bold" if bold else "normal")
        return tk.Label(parent, text=text, font=font, bg=parent['bg'], fg="#003366")

    def styled_button(self, parent, text, command):
        return tk.Button(parent,
                         text=text,
                         command=command,
                         bg="#003366",
                         fg="white",
                         font=("Segoe UI", 10, "bold"),
                         activebackground="#005580",
                         activeforeground="white",
                         relief="flat",
                         bd=0,
                         padx=10,
                         pady=6,
                         cursor="hand2")

    def login_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.master, bg="#e6f2ff")
        frame.pack(pady=50)

        self.styled_label(frame, "🔐 Login", 16, True).pack(pady=10)
        self.styled_label(frame, "Customer ID").pack()
        self.customer_id_entry = tk.Entry(frame)
        self.customer_id_entry.pack(pady=5)
        self.styled_label(frame, "Password").pack()
        self.password_entry = tk.Entry(frame, show='*')
        self.password_entry.pack(pady=5)
        self.styled_button(frame, "Login", self.login).pack(pady=10)

    def login(self):
        cid = self.customer_id_entry.get()
        pwd = self.password_entry.get()
        self.user = bank.login(cid, pwd)
        if self.user:
            self.popup("✅ Login successful!")
            self.master.after(1000, self.dashboard)
        else:
            self.popup("❌ Invalid credentials", success=False)

    def logout(self):
        self.popup("🔒 Logged out")
        self.master.after(1000, self.login_screen)

    def dashboard(self):
        self.clear_screen()
        frame = tk.Frame(self.master, bg="#e6f2ff")
        frame.pack(pady=30)

        self.styled_label(frame, f"Welcome, {self.user.name} 👋", 14, True).pack(pady=10)
        self.styled_button(frame, "Check Balance", self.show_balance).pack(pady=6)
        self.styled_button(frame, "Deposit", self.deposit_screen).pack(pady=6)
        self.styled_button(frame, "Withdraw", self.withdraw_screen).pack(pady=6)
        self.styled_button(frame, "Transfer", self.transfer_screen).pack(pady=6)
        self.styled_button(frame, "Logout", self.logout).pack(pady=10)

    def show_balance(self):
        balance = self.user.account.balance
        self.popup(f"💰 Balance: ${balance:.2f}")

    def deposit_screen(self):
        self.transaction_screen("Deposit", self.deposit)

    def withdraw_screen(self):
        self.transaction_screen("Withdraw", self.withdraw)

    def transfer_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.master, bg="#e6f2ff")
        frame.pack(pady=40)

        self.styled_label(frame, "🔁 Transfer Funds", 14, True).pack(pady=10)
        self.styled_label(frame, "Recipient ID").pack()
        recipient_entry = tk.Entry(frame)
        recipient_entry.pack(pady=5)
        self.styled_label(frame, "Amount").pack()
        amount_entry = tk.Entry(frame)
        amount_entry.pack(pady=5)

        self.styled_button(frame, "Transfer", lambda: self.transfer(recipient_entry.get(), amount_entry.get())).pack(pady=6)
        self.styled_button(frame, "Back", lambda: [self.popup("🔙 Back to dashboard"), self.master.after(1000, self.dashboard)]).pack(pady=10)

    def deposit(self, amount):
        try:
            if self.user.account.deposit(float(amount)):
                self.popup("✅ Deposit successful")
            else:
                self.popup("❌ Invalid amount", success=False)
        except:
            self.popup("❌ Enter a valid number", success=False)
        self.master.after(1000, self.dashboard)

    def withdraw(self, amount):
        try:
            if self.user.account.withdraw(float(amount)):
                self.popup("✅ Withdrawal successful")
            else:
                self.popup("❌ Insufficient balance", success=False)
        except:
            self.popup("❌ Enter a valid number", success=False)
        self.master.after(1000, self.dashboard)

    def transfer(self, recipient_id, amount):
        recipient = bank.customers.get(recipient_id)
        try:
            if recipient:
                if self.user.account.transfer(recipient.account, float(amount)):
                    self.popup("✅ Transfer successful")
                else:
                    self.popup("❌ Insufficient balance", success=False)
            else:
                self.popup("❌ Recipient not found", success=False)
        except:
            self.popup("❌ Invalid amount", success=False)
        self.master.after(1000, self.dashboard)

    def transaction_screen(self, title, action_function):
        self.clear_screen()
        frame = tk.Frame(self.master, bg="#e6f2ff")
        frame.pack(pady=50)

        self.styled_label(frame, f"{title} Amount", 14, True).pack(pady=10)
        amount_entry = tk.Entry(frame)
        amount_entry.pack(pady=5)
        self.styled_button(frame, "Submit", lambda: action_function(amount_entry.get())).pack(pady=6)
        self.styled_button(frame, "Back", lambda: [self.popup("🔙 Back to dashboard"), self.master.after(1000, self.dashboard)]).pack(pady=10)

    def popup(self, message, success=True):
        AnimatedPopup(self.master, message, success)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Start the app
root = tk.Tk()
app = BankingApp(root)
root.mainloop()
