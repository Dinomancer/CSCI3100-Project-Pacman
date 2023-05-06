#for the pop up window
import PySimpleGUI as Message

def response(self, text, windowname):
    layout = [[Message.Text(text)],
                  [Message.Button('OK')]]
    window = Message.Window(windowname, layout)
    while True:
        event, values = window.read()
        if event == Message.WIN_CLOSED or event == 'OK':  # if user closes window or clicks cancel
            break
    window.close()
