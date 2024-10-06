import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from Functions import resource_path
import ctypes
import sys

global partNum_input
global counterbalance_input
global code_input
global age_input
global gender_input
global handedness_input
global informed_consent

true_res = (ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1))

demographics_font_size = int(12)


def close_programms():
    close_programms = tk.Tk()
    close_programms.attributes("-fullscreen", True)
    close_programms.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 2)))
    close_programms.title("WICHTIG!")

    close_label = tk.Label(close_programms, justify="left",
                           text="Bitte beende alle nicht notwendigen Anwendungen "
                                "(Browser, Programme etc.), bevor Du mit dem "
                                "Experiment loslegst.\n\nSchließe bitte zudem Deinen Laptop an das Stromnetz an.",
                           font=("Arial", demographics_font_size))
    close_label.grid(row=1, column=0, columnspan=6,
                     pady=ctypes.windll.user32.GetSystemMetrics(0) // 10,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 2.0)

    def continue_click():
        close_programms.destroy()

    def abort_click():
        close_programms.destroy()
        sys.exit()

    continue_button = tk.Button(close_programms,
                                text="Hier klicken, wenn Du alle nicht notwendigen Anwendungen\n"
                                     "beendet hast!",
                                pady=1, command=continue_click,
                                font=("Arial", demographics_font_size), bd=10,
                                bg="lightgreen")
    continue_button.grid(row=3, column=2, columnspan=2,
                         pady=10)

    abort_button = tk.Button(close_programms,
                             text="Hier klicken, wenn Du erst noch mal checken willst, \n"
                                  "ob auch wirklich alle nicht notwendigen Anwendungen\n"
                                  "beendet wurden. Danach kannst Du das Experiment \n"
                                  "einfach neu starten.",
                             pady=1, command=abort_click,
                             font=("Arial", demographics_font_size), bd=10,
                             bg="red")
    abort_button.grid(row=5, column=2, columnspan=2,
                      pady=10)

    close_programms.mainloop()


def display_informed_consent():
    infCons = tk.Tk()
    infCons.attributes("-fullscreen", True)

    inst_label = tk.Label(infCons, justify="left",
                          text="Bitte lies Dir die folgenden Informationen genau durch. Du kannst den Text mit dem Mausrad oder der Scrollleiste rechts verschieben.\n"
                               "Klicke anschließend bitte auf den für Dich zutreffenden Button unterhalb des Textes.",
                          font=("Arial", demographics_font_size, "bold"),
                          height=3,
                          anchor="center")
    inst_label.pack(expand=True, fill=tk.X, side=tk.TOP)

    main_frame = tk.Frame(infCons)
    main_frame.pack(fill=tk.BOTH, expand=1)

    my_canvas = tk.Canvas(main_frame,
                          width=ctypes.windll.user32.GetSystemMetrics(
                              0) // 1.5,
                          height=int(ctypes.windll.user32.GetSystemMetrics(
                              1)) * 0.60)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL,
                                 command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox("all")))

    def _on_mousewheel(event):
        my_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    second_frame = tk.Frame(my_canvas)

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    def continue_click():
        global informed_consent
        informed_consent = 1
        infCons.destroy()

    def abort_click():
        global informed_consent
        informed_consent = 0
        infCons.destroy()
        sys.exit()

    scale_w = int(int(1.1 * 826) * (true_res[0] / 1920))
    scale_h = int(int(1.1 * 1169) * (true_res[1] / 1080))

    informed_1 = Image.open(
        resource_path("pics\\InformierteEinwilligung_short_1.ppm"))
    informed_1 = informed_1.resize((scale_w, scale_h), Image.ANTIALIAS)
    informed_1 = ImageTk.PhotoImage(informed_1)

    my_canvas.create_image(
        (ctypes.windll.user32.GetSystemMetrics(0) // 2 - scale_w // 2,
         int(ctypes.windll.user32.GetSystemMetrics(
             1) // 12)),
        anchor="nw", image=informed_1)

    informed_2 = Image.open(
        resource_path("pics\\InformierteEinwilligung_short_2.ppm"))
    informed_2 = informed_2.resize((scale_w, scale_h), Image.ANTIALIAS)
    informed_2 = ImageTk.PhotoImage(informed_2)

    my_canvas.create_image(
        (ctypes.windll.user32.GetSystemMetrics(0) // 2 - scale_w // 2,
         int(ctypes.windll.user32.GetSystemMetrics(
             1) // 12) + scale_h + 50),
        anchor="nw", image=informed_2)

    informed_3 = Image.open(
        resource_path("pics\\InformierteEinwilligung_short_3.ppm"))
    informed_3 = informed_3.resize((scale_w, scale_h), Image.ANTIALIAS)
    informed_3 = ImageTk.PhotoImage(informed_3)

    my_canvas.create_image(
        (ctypes.windll.user32.GetSystemMetrics(0) // 2 - scale_w // 2,
         int(ctypes.windll.user32.GetSystemMetrics(
             1) // 12) + 2 * scale_h + 100),
        anchor="nw", image=informed_3)

    approve_button = tk.Button(infCons, text="""
    Mit meinem Mausklick auf diesen Button erkläre ich mich damit einverstanden, an der Studie teilzunehmen. Ich bin über Ziele\n
    und Ablauf der Studie informiert worden und habe diese verstanden. Meine Teilnahme erfolgt freiwillig. Ich habe das Recht,\n 
    die Teilnahme jederzeit und ohne Angabe von Gründen aufzukündigen. Ich bin außerdem mit einer Verwendung der Forschungsdaten\n 
    in anonymisierter Form einverstanden. Ich wurde über die Verwendung von personenbezogenen Daten und meine Rechte diesbezüglich\n
    aufgeklärt und bin damit ebenfalls einverstanden.\n""",
                               command=continue_click,
                               font=(
                                   "Arial", demographics_font_size - 2,
                                   "bold"),
                               anchor="center", height=18,
                               bd=10,
                               justify="left", bg="lightgreen")
    approve_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

    disapprove_button = tk.Button(infCons, text="""
    Da ich mit den Teilnahmebedingungen nicht\n
    einverstanden bin, breche ich meine Teilnahme\n
    an diesem Versuch durch Mausklick auf diesen\n
    Button ab.""",
                                  command=abort_click,
                                  font=(
                                      "Arial", demographics_font_size - 2,
                                      "bold"),
                                  anchor="center", height=18,
                                  bd=10,
                                  justify="left", bg="red")
    disapprove_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    infCons.mainloop()

    return informed_consent


def select_partNum_counterbalance():
    demo = tk.Tk()
    demo.attributes("-fullscreen", True)
    demo.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    demo.title("Willkommen!")

    partNum_label = tk.Label(demo, justify="left",
                          text="Bitte Versuchspersonennummer (Zahl) eingeben:"
                               "\n",
                          font=("Arial", demographics_font_size))
    partNum_label.grid(row=1, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=25)
    partNum = tk.Text(demo, height=1, width=10,
                  font=("Arial", demographics_font_size))
    partNum.config(font=("Arial", demographics_font_size))
    partNum.grid(row=2, column=1, columnspan=1,
             padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    counterbalance_label = tk.Label(demo, justify="left",
                             text="Bitte Counterbalance (1, 2, 3, 4) eingeben:"
                                  "\n",
                             font=("Arial", demographics_font_size))
    counterbalance_label.grid(row=3, column=1, columnspan=1,
                       padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                       pady=25)
    counterbalance = tk.Text(demo, height=1, width=10,
                      font=("Arial", demographics_font_size))
    counterbalance.config(font=("Arial", demographics_font_size))
    counterbalance.grid(row=4, column=1, columnspan=1,
                 padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    changeFreq_label = tk.Label(demo, justify="left",
                                    text="Bitte Change-Bedingung (L oder H) eingeben:"
                                         "\n",
                                    font=("Arial", demographics_font_size))
    changeFreq_label.grid(row=5, column=1, columnspan=1,
                              padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                              pady=25)
    changeFreq = tk.Text(demo, height=1, width=10,
                             font=("Arial", demographics_font_size))
    changeFreq.config(font=("Arial", demographics_font_size))
    changeFreq.grid(row=6, column=1, columnspan=1,
                        padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    def continue_click(_event=None):
        global partNum_input
        global counterbalance_input
        global changeFreq_input

        partNum_input = partNum.get("1.0", "end-1c")
        counterbalance_input = counterbalance.get("1.0", "end-1c")
        changeFreq_input = changeFreq.get("1.0", "end-1c")

        try:
            if isinstance(int(partNum_input), int) and counterbalance_input in ("1", "2", "3", "4") and \
                    changeFreq_input in ("L", "H"):
                demo.destroy()
        except Exception:
            print("Falsche Eingabe, bitte bei Versuchspersonennummer eine ganze Zahl und bei Bedingung 1 oder 2 eingeben\n"
                  "(keine Leerzeichen o.ä.!)")

    empty_label = tk.Label(demo, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=7, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(demo, text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=8, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)
    demo.bind("<F8>", continue_click)
    demo.focus_set()

    demo.mainloop()

    return partNum_input, counterbalance_input, changeFreq_input


def create_id_code():
    demo = tk.Tk()
    demo.attributes("-fullscreen", True)
    demo.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    demo.title("Willkommen!")

    code_label = tk.Label(demo, justify="left",
                          text="Bitte gib Deinen individuellen Versuchspersonen-Code ein. Dieser setzt sich aus folgenden Bestandteilen zusammen:\n\n"
                               "1. Tag Deines Geburtstages (z.B. 03 wenn Du am 03.06. Geburtstag hast)\n"
                               "2. Erster Buchstabe Deines Lieblingsgerichts (z.B. P wenn Du am liebsten Pfannkuchen isst)\n"
                               "3. Letzter Buchstabe Deines Nachnamens (z.B. R wenn Dein Nachname Müller ist)\n"
                               "4. Erster Buchstabe des Vornamens Deiner Mutter (z.B. P wenn Sie Petra heißt)\n\n"
                               ""
                               "Der Code, der sich aus den Beispielen in Klammern zusammensetzt, wäre demnach:\n\n"
                               "03PRP\n\n"
                               "Bitte achte darauf, dass Du den Code korrekt eingibst. Wir benötigen ihn, damit wir Deine Datensätze\n"
                               "später korrekt zusammenführen können. Das Programm sollte eine Textdatei mit dem Code, den Du am ersten\n"
                               "Termin angegeben hast, anlegen. Schreibe ihn Dir trotzdem am besten auf, da das nicht immer klappt. Danke! :)"
                               "\n",
                          font=("Arial", demographics_font_size))
    code_label.grid(row=1, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=25)

    code = tk.Text(demo, height=1, width=10,
                   font=("Arial", demographics_font_size))
    code.config(font=("Arial", demographics_font_size))
    code.grid(row=2, column=1, columnspan=1,
              padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    def continue_click(_event=None):
        global code_input

        code_input = code.get("1.0", "end-1c")

        if len(code_input) == 5:
            demo.destroy()

    empty_label = tk.Label(demo, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=3, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(demo, text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=4, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    demo.bind("<F8>", continue_click)
    demo.focus_set()

    demo.mainloop()

    return code_input


def collect_demographics():
    demo = tk.Tk()
    demo.attributes("-fullscreen", True)
    demo.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    demo.title("Willkommen!")

    inst_label = tk.Label(demo, justify="left",
                          text="Bevor es losgehen kann, benötigen wir noch einige Angaben über Deine Person."
                               "\n",
                          font=("Arial", demographics_font_size))
    inst_label.grid(row=1, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=25)

    age_label = tk.Label(demo, justify="left",
                         text="Bitte gib Dein Alter (in Jahren) an: ",
                         font=("Arial", demographics_font_size))
    age_label.grid(row=2, column=1, columnspan=1,
                   padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                   pady=10)
    age = tk.Text(demo, height=1, width=10,
                  font=("Arial", demographics_font_size))
    age.config(font=("Arial", demographics_font_size))
    age.grid(row=3, column=1, columnspan=1,
             padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    gender_label = tk.Label(demo, justify="left",
                            text="Bitte wähle Dein Geschlecht aus:",
                            font=("Arial", demographics_font_size))
    gender_label.grid(row=4, column=1, columnspan=1,
                      padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                      pady=10)
    gender_selected = tk.StringVar()
    gender_selected.set("Bitte auswählen")
    gender = tk.OptionMenu(demo, gender_selected, "Männlich", "Weiblich",
                           "Divers")
    gender.config(font=("Arial", demographics_font_size))
    gender.grid(row=5, column=1, columnspan=1,
                padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    handedness_label = tk.Label(demo, justify="left",
                                text="Bitte wähle Deine Händigkeit aus:",
                                font=("Arial", demographics_font_size))
    handedness_label.grid(row=6, column=1, columnspan=1,
                          padx=ctypes.windll.user32.GetSystemMetrics(
                              1) // 1.75,
                          pady=10)
    handedness_selected = tk.StringVar()
    handedness_selected.set("Bitte auswählen")
    handedness = tk.OptionMenu(demo, handedness_selected, "Rechts", "Links",
                               "Beidhändig")
    handedness.config(font=("Arial", demographics_font_size))
    handedness.grid(row=7, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=10)

    def continue_click(_event=None):
        global age_input
        global gender_input
        global handedness_input

        age_input = age.get("1.0", "end-1c")
        gender_input = gender_selected.get()
        handedness_input = handedness_selected.get()

        if len(age_input) > 0 and \
                gender_input != "Bitte auswählen" and handedness_input != "Bitte auswählen":
            demo.destroy()

    empty_label = tk.Label(demo, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=10, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(demo, text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=11, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    demo.bind("<F8>", continue_click)
    demo.focus_set()

    demo.mainloop()

    return age_input, gender_input, handedness_input


def display_id(participant_id):
    part_id = tk.Tk()
    part_id.attributes("-fullscreen", True)
    part_id.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 2)))
    part_id.title("WICHTIG!")

    id_label = tk.Label(part_id, justify="left",
                        text="Bitte berücksichtige, dass Du nur mit einer Anmeldung für diesen Versuch\n"
                             "auf SONA teilnehmen solltest, da Du nur in diesem Fall berechtigt bist,\n"
                             "die Teilnahmekompensation für diesen Versuch zu erhalten.\n"
                             "Hast Du keinen SONA-Account und bist nicht angemeldet, können wir Dir\n"
                             "leider keine Teilnahmekompensation gewähren. In diesem Fall solltest\n"
                             "Du den Versuch im nächsten Schritt abbrechen und Dich erst auf SONA\n"
                             "anmelden:\n\n"
                             "https://psywue.sona-systems.com/default.aspx\n\n"
                             "",
                        font=("Arial", demographics_font_size, "bold"))
    id_label.grid(row=1, column=1, columnspan=1,
                  padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.625,
                  pady=100)

    def continue_click(_event=None):
        part_id.destroy()

    empty_label = tk.Label(part_id, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=2, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)

    continue_button = tk.Button(part_id, text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=3, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    part_id.bind("<F8>", continue_click)
    part_id.focus_set()

    part_id.mainloop()
