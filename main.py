"""
This script is main application script. It configures connection with a controller over serial, sets up GUI
and manages data exchange between controller and program interface.

"""

import tkinter as tk
import connection_frame  as connection_frame
import time


class Main:
    def __init__(self):
        """The initialization of a program

        Define global program variables.

        """
        self.serial = None
        self.top = tk.Tk()
        self.checks = []
        self.last_check_ind = 0
        self.alphabet = [
            0b0000000000000001,
            0b0000000000000010,
            0b0000000000000100,
            0b0000000000001000,
            0b0000000000010000,
            0b0000000000100000,
            0b0000000001000000,
            0b0000000010000000,
            0b0000000100000000,
            0b0000001000000000,
            0b0000010000000000,
            0b0000100000000000,
            0b0001000000000000,
            0b0010000000000000,
            0b0100000000000000,
            0b1000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0000000000000000,
            0b0001001011001001,
            0b0001010111000000,
            0b0001001011111001,
            0b0000000011100011,
            0b0000010100110000,
            0b0001001011001000,
            0b0011101000000000,
            0b0001011100000000,
            0b0000000000000000, #
            0b0000000000000110, # !
            0b0000001000100000, # "
            0b0001001011001110, # #
            0b0001001011101101, # $
            0b0000110000100100, # %
            0b0010001101011101, # &
            0b0000010000000000, # '
            0b0010010000000000, # (
            0b0000100100000000, # )
            0b0011111111000000, # *
            0b0001001011000000, # +
            0b0000100000000000, # ,
            0b0000000011000000, # -
            0b0000000000000000, # .
            0b0000110000000000, # /
            0b0000110000111111, # 0
            0b0000000000000110, # 1
            0b0000000011011011, # 2
            0b0000000010001111, # 3
            0b0000000011100110, # 4
            0b0000000011101101, # 5
            0b0000000011111101, # 6
            0b0000000000000111, # 7
            0b0000000011111111, # 8
            0b0000000011101111, # 9
            0b0001001000000000, # :
            0b0000101000000000, # ;
            0b0010010000000000, # <
            0b0000000011001000, # =
            0b0000100100000000, # >
            0b0001000010000011, # ?
            0b0000001010111011, # @
            0b0000000011110111, # A
            0b0001001010001111, # B
            0b0000000000111001, # C
            0b0001001000001111, # D
            0b0000000011111001, # E
            0b0000000001110001, # F
            0b0000000010111101, # G
            0b0000000011110110, # H
            0b0001001000000000, # I
            0b0000000000011110, # J
            0b0010010001110000, # K
            0b0000000000111000, # L
            0b0000010100110110, # M
            0b0010000100110110, # N
            0b0000000000111111, # O
            0b0000000011110011, # P
            0b0010000000111111, # Q
            0b0010000011110011, # R
            0b0000000011101101, # S
            0b0001001000000001, # T
            0b0000000000111110, # U
            0b0000110000110000, # V
            0b0010100000110110, # W
            0b0010110100000000, # X
            0b0001010100000000, # Y
            0b0000110000001001, # Z
            0b0000000000111001, # [
            0b0010000100000000, #
            0b0000000000001111, # ]
            0b0000110000000011, # ^
            0b0000000000001000, # _
            0b0000000100000000, # `
            0b0001000001011000, # a
            0b0010000001111000, # b
            0b0000000011011000, # c
            0b0000100010001110, # d
            0b0000100001011000, # e
            0b0000000001110001, # f
            0b0000010010001110, # g
            0b0001000001110000, # h
            0b0001000000000000, # i
            0b0000000000001110, # j
            0b0011011000000000, # k
            0b0000000000110000, # l
            0b0001000011010100, # m
            0b0001000001010000, # n
            0b0000000011011100, # o
            0b0000000101110000, # p
            0b0000010010000110, # q
            0b0000000001010000, # r
            0b0010000010001000, # s
            0b0000000001111000, # t
            0b0000000000011100, # u
            0b0010000000000100, # v
            0b0010100000010100, # w
            0b0010100011000000, # x
            0b0010000000001100, # y
            0b0000100001001000, # z
            0b0000100101001001, # {
            0b0001001000000000, # |
            0b0010010010001001, # }
            0b0000010100100000, # ~
            0b0011111111111111]

    def start(self):
        """The starting point of a program

        Set up program interface.

        :return:
        """
        connection_frame.Connection(self).draw()
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.top.mainloop()

    def on_closing(self):
        """Define behaviour when application is closed

        Cut off connection over serial and close application interface.

        :return:
        """
        if self.serial is not None:
            self.serial.close()
        self.top.destroy()

    def get_frame(self):
        """Get main application frame

        :return: Tk Widget
            Main window of an application
        """
        return self.top

    def on_connect(self, ser, model):
        """Define behaviour when user is trying to connect to a serial port

        Set the desired port to a global variable
        Convert characters of a model to an integers according to mapping array.

        :param ser: The desired port for connection
        :param model: A string to be sent over serial
        :return:
        """
        self.serial = ser
        for i in range(len(model)):
            bitarray = self.alphabet[ord(model[i])]
            self.serial.write(bitarray)
            self.serial.flush()

    def update_model(self, model):
        """Update model of transferred data and send it over serial

        Convert characters of a model to an integers according to mapping array.

        :param model: A string to be sent over serial
        :return:
        """
        for i in range(len(model)):
            bitarray = self.alphabet[ord(model[i])]
            self.serial.write(str(bitarray).encode("utf-8"))

    def update_frequency(self, freq, duty, model):
        """Send new electrical parameters over serial

        :param freq:
        :param duty:
        :return:
        """
        msg = "f" + str(freq) + "d" + str(duty) + "m" + str(self.alphabet[ord(model)])
        self.serial.write(msg.encode("utf-8"))


    def select(self, i):
        """Select particular segment to be turned on

        N.B. This is for working with 3x3 electrode

        :param i: the index of a segment
        :return:
        """
        self.serial.write(("+" + str(i)).encode("utf-8"))
        self.serial.flush()
        self.checks[i][0].select()

    def deselect(self, i):
        """Select particular segment to be turned off

        N.B. This is for working with 3x3 electrode

        :param i: the index of a segment
        :return:
        """
        self.serial.write(("-" + str(i)).encode("utf-8"))
        self.serial.flush()
        self.checks[i][0].deselect()

    def state(self, i):
        """Get the state of a particular segment

        N.B. This is for working with 3x3 electrode

        :param i: the index of a segment
        :return: the binary value indicating if a particular segment is on
        """
        return self.checks[i][1].get()

    def toggle(self, i):
        """Change the state of a particular segment

        N.B. This is for working with 3x3 electrode

        :param i: the index of a segment
        :return:
        """
        if self.state(i) == 1:
            self.deselect(i)
        else:
            self.select(i)

def checkbox_changed(port, var, ser):
    """Send updated information about enabling particular port over serial

    N.B. This is for working with 3x3 electrode

    :param port: index of a port
    :param var: binary value indicating the desired state of a port
    :param ser: the serial over which to send the data
    :return:
    """
    def f():
        to_send = "-"
        if var.get() == 1:
            to_send = "+"
            print("checked " + str(port))
        else:
            to_send = "-"
            print("unchecked " + str(port))
        to_send += str(port) + "\n"
        ser.write(to_send.encode("utf-8"))
        ser.flush()

    return f


def main():
    Main().start()


main()
