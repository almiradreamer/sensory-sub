"""
This script draws application interface and manages user manipulations with it.

"""

import tkinter as tk
import subprocess
import serial
import pickle
from PIL import Image, ImageFont, ImageDraw, ImageTk


class Connection:
    def __init__(self, parent):
        """The initialization of a program

        Define global program variables.

        """
        self.parent = parent
        parent_frame = self.parent.get_frame()
        self.text_frame = tk.Frame(parent_frame)
        self.text_frame.grid(row=1, padx=10, pady=10)
        self.model_frame = tk.Frame(parent_frame)
        self.model_frame.grid(row=2, padx=10, pady=10)
        self.connect_frame = tk.Frame(parent_frame)
        self.connect_frame.grid(row=0, padx=10, pady=10)
        self.electric_frame = tk.Frame(parent_frame)
        self.electric_frame.grid(row=4, padx=10, pady=10)

        self.freq_edit = tk.Entry(self.electric_frame)
        self.duty_edit = tk.Entry(self.electric_frame)

        self.ports_listbox = tk.Listbox(self.connect_frame)

        self.text_transfer = tk.Entry(self.text_frame)

        self.model_image = tk.Label(self.model_frame)
        self.model_image.grid(row=0, column=1)

        self.model = ''
        self.counter = 0
        self.font14 = ImageFont.truetype('Segment14.otf', 64)

    def draw(self):
        """Draw application interface

        Draw initial state of Connection Frame, Text Transfer Frame and Electrical Parameters Frame

        :return:
        """

        self.text_transfer.config(validate="focusout", validatecommand=self.reset_counter)
        self.text_transfer.delete(0, tk.END)
        tk.Label(self.text_frame, text="Letter to send: ").grid(row=1)
        self.text_transfer.grid(row=1, column=1)
        send_text_button = tk.Button(self.text_frame, text="Send", width=10, command=self.send_text())
        send_text_button.grid(row=1, column=4, pady=20, padx=20)
        tk.Button(self.text_frame, text="<", width=2, command=self.update_counter(-1)).grid(row=1, column=2)
        tk.Button(self.text_frame, text=">", width=2, command=self.update_counter(1)).grid(row=1, column=3)

        available_serials = get_available_serials()

        for i in range(len(available_serials)):
            self.ports_listbox.insert(i + 1, available_serials[i])

        self.connect_msg = tk.Label(self.connect_frame, text="Port: ").grid(row=1)
        self.ports_listbox.grid(row=1, column=1)
        self.connect_button = tk.Button(self.connect_frame, text="Connect", width=10, command=self.connect())
        self.connect_button.grid(row=1, column=2, pady=20, padx=20)
        tk.Label(self.connect_frame, text="Connection Parameters", font=(None, 16)).grid(row=0, padx=15, pady=15)
        tk.Label(self.text_frame, text="Text Transfer", font=(None, 16)).grid(row=0, padx=15, pady=15)
        tk.Label(self.electric_frame, text="Electric Parameters", font=(None, 16)).grid(row=0, padx=15, pady=15)
        self.freq_edit.delete(0, tk.END)
        self.freq_edit.delete(0, tk.END)
        tk.Label(self.electric_frame, text="Frequency: ").grid(row=1)
        self.freq_edit.grid(row=1, column=1)
        tk.Label(self.electric_frame, text="Duty ratio: ").grid(row=2)
        self.duty_edit.grid(row=2, column=1)
        change_freq_button = tk.Button(self.electric_frame, text="Set", width=10, command=self.set_frequency(), padx=10)
        change_freq_button.grid(column=2)
        file = open(r'params.pkl', 'rb')
        freq = pickle.load(file)
        duty = pickle.load(file)
        print ("freq is ", freq)
        print ("duty is ", duty)
        self.freq_edit.insert(0, freq)
        self.duty_edit.insert(0, duty)
        file.close()

    def send_text(self):
        """Handle a text submitted by a user

        Send a string from user input to the top frame to handle further transfer to a controller.
        Draw a preview of a text using 14-segment font.

        :return:
        """
        def f():
            self.highlight_input()
            text = self.text_transfer.get()[self.counter]
            self.model = text
            # print("yep")
            self.parent.update_model(self.model.upper())
            print(self.model)
        return f

    def update_counter(self, delta):
        """Handle a walk through input string

        Set new counter that indicates the current character to be sent

        :param delta: the integer indicating how user wants to change the focus character
        :return:
        """
        def f():
            text = self.text_transfer.get()
            counter = self.counter + delta
            if len(text) > 0:
                if 0 <= counter < len(text):
                    self.counter = counter
                    self.highlight_input()
                else:
                    self.counter = 0
                    self.highlight_input()
        return f

    def reset_counter(self):
        """Reset counter that indicates the current character to be sent

        :return:
        """
        self.counter = 0
        self.highlight_input()

    def highlight_input(self):
        """Highlight the focus character in the input string

        :return:
        """
        text = self.text_transfer.get()
        if 0 <= self.counter < len(text):
            text = text.lower()
            text = text[:self.counter] + text[self.counter].upper() + text[self.counter + 1:]
            self.text_transfer.delete(0, tk.END)
            self.text_transfer.insert(0, text)
            tk.Label(self.model_frame, text="Preview: ").grid(row=0, column=0)
            width, height = self.font14.getsize(text[self.counter].upper())
            image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), text[self.counter].upper(), font=self.font14, fill="black")
            self._photoimage = ImageTk.PhotoImage(image)
            self.model_image.config(image=self._photoimage)
        else:
            self.counter = 0
            self.highlight_input()

    def set_frequency(self):
        """Handle a new electrical parameters submitted by a user

        Send new frequency and duty ration from user input to the top frame to handle further transfer to a controller.

        :return:
        """
        def f():
            freq = float(self.freq_edit.get())
            duty = float(self.duty_edit.get())
            if duty == 0:
                duty = 1
            if duty > 1:
                duty = duty / 100
            self.parent.update_frequency(freq, duty, self.model.upper())
        return f

    def connect(self):
        """Handle the connection button

        Define a serial over which program is connected to the desired by a user port

        :return:
        """
        def f():
            com_port = self.ports_listbox.get(tk.ACTIVE)
            ser = serial.Serial(com_port)
            print("connected to :" + ser.name)
            self.connect_msg = tk.Label(self.connect_frame, text="Connected to :" + ser.name).grid(row=1)
            self.parent.on_connect(ser, self.model)
            self.ports_listbox.destroy()
            self.connect_button.destroy()
        return f

    def checkbox_changed(self, i, j, var):
        """Handle a new checkbox submitted by a user

        N.B. This is for working with 3x3 electrode

        :param i: the index of a row of the checkbox
        :param j: the index of a column of the checkbox
        :param var: the binary value indicating the new value for the segment
        :return:
        """
        def f():
            self.model[i][j] = var.get()
        return f


def get_available_serials():
    """Get available for connection ports

    :return: List of available ports
    """
    ports_string = subprocess.check_output(['python3', '-m', 'serial.tools.list_ports']).decode("utf-8").strip()
    print("FOUND: " + ports_string)
    if len(ports_string) == 0:
        print("stubs used as no ports found")
        return ["/dev/ttyUSB0", "/dev/ttyUSB1"]
    return ports_string.split('\n')
