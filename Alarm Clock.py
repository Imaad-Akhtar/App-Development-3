import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("300x400")

        self.current_time_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.current_time_label.pack(pady=20)

        self.set_alarm_button = tk.Button(root, text="Set Alarm", command=self.open_set_alarm_window)
        self.set_alarm_button.pack(pady=10)

        self.alarms_frame = tk.Frame(root)
        self.alarms_frame.pack(pady=20)

        self.alarms = []

        self.update_time()

    def update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=now)
        self.check_alarms(now)
        self.root.after(1000, self.update_time)

    def open_set_alarm_window(self):
        set_alarm_window = tk.Toplevel(self.root)
        set_alarm_window.title("Set Alarm")

        time_label = tk.Label(set_alarm_window, text="Time (HH:MM)", font=("Helvetica", 14))
        time_label.pack(pady=10)

        self.time_entry = tk.Entry(set_alarm_window, font=("Helvetica", 14))
        self.time_entry.pack(pady=10)

        tone_label = tk.Label(set_alarm_window, text="Tone", font=("Helvetica", 14))
        tone_label.pack(pady=10)

        self.tone_entry = tk.Entry(set_alarm_window, font=("Helvetica", 14))
        self.tone_entry.pack(pady=10)

        save_button = tk.Button(set_alarm_window, text="Save", command=self.save_alarm)
        save_button.pack(pady=10)

    def save_alarm(self):
        alarm_time = self.time_entry.get()
        alarm_tone = self.tone_entry.get()

        if not alarm_time:
            messagebox.showwarning("Input Error", "Please enter a time for the alarm.")
            return

        try:
            datetime.strptime(alarm_time, "%H:%M")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid time in HH:MM format.")
            return

        alarm = {"time": alarm_time, "tone": alarm_tone, "active": True}
        self.alarms.append(alarm)
        self.update_alarms_list()

    def update_alarms_list(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()

        for i, alarm in enumerate(self.alarms):
            alarm_text = f"{alarm['time']} - {alarm['tone']}"
            alarm_label = tk.Label(self.alarms_frame, text=alarm_text, font=("Helvetica", 12))
            alarm_label.grid(row=i, column=0, padx=10)

            toggle_button = tk.Button(self.alarms_frame, text="On" if alarm["active"] else "Off",
                                      command=lambda i=i: self.toggle_alarm(i))
            toggle_button.grid(row=i, column=1, padx=10)

            delete_button = tk.Button(self.alarms_frame, text="Delete", command=lambda i=i: self.delete_alarm(i))
            delete_button.grid(row=i, column=2, padx=10)

    def toggle_alarm(self, index):
        self.alarms[index]["active"] = not self.alarms[index]["active"]
        self.update_alarms_list()

    def delete_alarm(self, index):
        del self.alarms[index]
        self.update_alarms_list()

    def check_alarms(self, current_time):
        current_time = current_time[:5]  # Strip seconds
        for alarm in self.alarms:
            if alarm["active"] and alarm["time"] == current_time:
                self.trigger_alarm(alarm)

    def trigger_alarm(self, alarm):
        alarm["active"] = False
        self.update_alarms_list()
        threading.Thread(target=self.show_alarm_popup, args=(alarm,)).start()

    def show_alarm_popup(self, alarm):
        messagebox.showinfo("Alarm", f"Alarm ringing! Tone: {alarm['tone']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
