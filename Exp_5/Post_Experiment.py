import tkinter as tk
import ctypes

demographics_font_size = int(12)

global hypothesis_input
global regularities_input
global strategy_input
global strategy_effort_input
global delayedPerc_input
global effort_input
global hold_flag
global perceptibility_input
global other_input
global diff_input
global participated_earlier_input


def post_experiment_part_one(total_score, total_falls, total_eaten):
    post_one = tk.Tk()
    post_one.attributes("-fullscreen", True)
    post_one.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_one.title("Fast geschafft!")

    inst_label = tk.Label(post_one, justify="left",
                          text="Der Hauptteil des Experiments ist nun vorbei. Du hast insgesamt\n\n" +
                               total_score + " Punkte gesammelt, bist\n\n" +
                               total_falls + "-mal weggeweht und\n\n" +
                               total_eaten + "-mal gefressen worden. Cool!\n\n"
                                             "Vielen Dank für Deine Teilnahme an diesem Teil!\n\n",
                          font=("Arial", demographics_font_size))
    inst_label.grid(row=1, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=25)

    def continue_click(_event=None):
        post_one.destroy()

    empty_label = tk.Label(post_one, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=4, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_one,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

    post_one.bind("<F8>", continue_click)
    post_one.focus_set()

    post_one.mainloop()


def post_experiment_questionnaire_one(total_score, total_falls, total_eaten):
    post_one = tk.Tk()
    post_one.attributes("-fullscreen", True)
    post_one.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_one.title("Fast geschafft! (1/6)")

    inst_label = tk.Label(post_one, justify="left",
                          text="Der Hauptteil des Experiments ist nun vorbei. Du hast insgesamt\n\n" +
                               total_score + " Punkte gesammelt, bist\n\n" +
                               total_falls + "-mal weggeweht und\n\n" +
                               total_eaten + "-mal gefressen worden. Beeindruckend!\n\n"
                                             "Vielen Dank für Deine Teilnahme an diesem Teil!\n\n"
                                             "Wir würden Dich nun noch bitten, die nachfolgenden Fragen zu\n"
                                             "beantworten, da Deine Antworten sehr wichtig für die Auswertung\n"
                                             "des Experiments für uns sind.",
                          font=("Arial", demographics_font_size))
    inst_label.grid(row=1, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=25)

    hypothesis_label = tk.Label(post_one, justify="left",
                                text="Was denkst Du war der Zweck dieses Experiments?",
                                font=("Arial", demographics_font_size))
    hypothesis_label.grid(row=2, column=1, columnspan=1,
                          padx=ctypes.windll.user32.GetSystemMetrics(
                              1) // 1.75,
                          pady=10)
    hypothesis = tk.Text(post_one, height=10, width=60,
                         font=("Arial", demographics_font_size))
    hypothesis.grid(row=3, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                    pady=10)
    hypothesis.insert(tk.INSERT, "")

    def continue_click(_event=None):
        global hypothesis_input

        hypothesis_input = hypothesis.get("1.0", "end-1c")
        post_one.destroy()

        return hypothesis_input

    empty_label = tk.Label(post_one, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=4, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_one,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

    post_one.bind("<F8>", continue_click)
    post_one.focus_set()

    post_one.mainloop()

    return hypothesis_input


def post_experiment_questionnaire_two():
    global regularities_input
    post_two = tk.Tk()
    post_two.attributes("-fullscreen", True)
    post_two.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_two.title("Fast geschafft! (2/6)")

    regularities_label = tk.Label(post_two, justify="left",
                                  text="Sind Dir während des Experiments bestimmte Regelmäßigkeiten\naufgefallen? "
                                       "Falls ja, welche?",
                                  font=("Arial", demographics_font_size))
    regularities_label.grid(row=1, column=1, columnspan=1,
                            padx=ctypes.windll.user32.GetSystemMetrics(
                                1) // 1.75,
                            pady=25)
    regularities = tk.Text(post_two, height=6, width=60,
                           font=("Arial", demographics_font_size))
    regularities.grid(row=2, column=1, columnspan=1,
                      padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                      pady=10)

    def continue_click(_event=None):
        global regularities_input

        regularities_input = regularities.get("1.0", "end-1c")

        post_two.destroy()

    empty_label = tk.Label(post_two, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=5, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_two,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=6, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    post_two.bind("<F8>", continue_click)
    post_two.focus_set()

    post_two.mainloop()

    return regularities_input


def post_experiment_questionnaire_three():
    global strategy_input
    global strategy_effort_input
    global delayedPerc_input

    post_three = tk.Tk()
    post_three.attributes("-fullscreen", True)
    post_three.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_three.title("Fast geschafft! (3/6)")

    strategy_label = tk.Label(post_three, justify="left",
                              text="Hast Du während des Experiments bestimmte Strategien angewandt?\n"
                                   "Falls ja, welche?",
                              font=("Arial", demographics_font_size))
    strategy_label.grid(row=1, column=1, columnspan=1,
                        padx=ctypes.windll.user32.GetSystemMetrics(
                            1) // 1.75,
                        pady=10)
    strategy = tk.Text(post_three, height=6, width=60,
                       font=("Arial", demographics_font_size))
    strategy.grid(row=2, column=1, columnspan=1,
                  padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                  pady=10)

    strategy_effort_label = tk.Label(post_three, justify="left",
                                     text="Wenn Du den unterschiedlichen Bewegungsaufwand für manche Sprünge bedenkst,\n"
                                          "beschreibe bitte kurz, wie dieser Aufwand Deine Strategie(n) beeinflusst hat.",
                                     font=("Arial", demographics_font_size))
    strategy_effort_label.grid(row=3, column=1, columnspan=1,
                               padx=ctypes.windll.user32.GetSystemMetrics(
                                   1) // 1.75,
                               pady=10)
    strategy_effort = tk.Text(post_three, height=6, width=60,
                              font=("Arial", demographics_font_size))
    strategy_effort.grid(row=4, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    delayedPerc_label = tk.Label(post_three, justify="left",
                                   text="In wie viel Prozent der Durchgänge, in denen die Punkte früher dargestellt wurden,\n"
                                        "hast Du Dich erst kurz vor dem Sprung für eine Sprungrichtung entschieden?",
                                   font=("Arial", demographics_font_size))
    delayedPerc_label.grid(row=5, column=1, columnspan=1,
                             padx=ctypes.windll.user32.GetSystemMetrics(
                                 1) // 1.75,
                             pady=10)
    delayedPerc_selected = tk.StringVar()
    delayedPerc_selected.set("Bitte auswählen")
    delayedPerc = tk.OptionMenu(post_three, delayedPerc_selected,
                                "0 %", "5 %", "10 %", "15 %", "20 %", "25 %", "30 %", "35 %", "40 %", "45 %", "50 %",
                                "55 %", "60 %", "65 %", "70 %", "75 %", "80 %", "85 %", "90 %", "95 %", "100 %")

    delayedPerc.config(font=("Arial", demographics_font_size))
    delayedPerc.grid(row=6, column=1, columnspan=1,
                padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                pady=10)

    def continue_click(_event=None):
        global strategy_input
        global strategy_effort_input
        global delayedPerc_input

        strategy_input = strategy.get("1.0", "end-1c")
        strategy_effort_input = strategy_effort.get("1.0", "end-1c")
        delayedPerc_input = delayedPerc_selected.get()

        if delayedPerc_input != "Bitte auswählen":
            post_three.destroy()

    empty_label = tk.Label(post_three, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=7, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_three,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20,
                                command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=8, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    post_three.bind("<F8>", continue_click)
    post_three.focus_set()

    post_three.mainloop()

    return strategy_input, strategy_effort_input, delayedPerc_input


def post_experiment_questionnaire_five():
    global diff_input
    global effort_input
    global hold_flag
    global perceptibility_input

    post_five = tk.Tk()
    post_five.attributes("-fullscreen", True)
    post_five.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_five.title("Fast geschafft! (5/6)")

    perceptibility_label = tk.Label(post_five, justify="left",
                                    text="Konntest Du während des Experiments stets alles gut erkennen\noder "
                                         "gab es Probleme bei der Darstellung bestimmter Elemente?",
                                    font=("Arial", demographics_font_size))
    perceptibility_label.grid(row=1, column=1, columnspan=1,
                              padx=ctypes.windll.user32.GetSystemMetrics(
                                  1) // 1.75, pady=25)
    perceptibility = tk.Text(post_five, height=5, width=60,
                             font=("Arial", demographics_font_size))
    perceptibility.grid(row=2, column=1, columnspan=1,
                        padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                        pady=10)

    diff_label = tk.Label(post_five, justify="left",
                          text="Wie schwierig fandest Du da das Experiment?",
                          font=("Arial", demographics_font_size))
    diff_label.grid(row=3, column=1, columnspan=1,
                    padx=ctypes.windll.user32.GetSystemMetrics(
                        1) // 1.75, pady=25)
    diff_selected = tk.StringVar()
    diff_selected.set("Bitte auswählen")
    diff = tk.OptionMenu(post_five, diff_selected, "1 (gar nicht schwierig)",
                         "2", "3", "4", "5",
                         "6", "7", "8", "9 (sehr schwierig)")
    diff.config(font=("Arial", demographics_font_size))
    diff.grid(row=4, column=1, columnspan=1,
              padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    effort_label = tk.Label(post_five, justify="left",
                            text="Wie sehr hast Du Dich bei der Durchführung des Experiments angestrengt?",
                            font=("Arial", demographics_font_size))
    effort_label.grid(row=5, column=1, columnspan=1,
                      padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                      pady=25)
    effort_selected = tk.StringVar()
    effort_selected.set("Bitte auswählen")
    effort = tk.OptionMenu(post_five, effort_selected,
                           "1 (gar nicht angestrengt)", "2", "3", "4", "5",
                           "6", "7", "8", "9 (sehr angestrengt)")
    effort.config(font=("Arial", demographics_font_size))
    effort.grid(row=6, column=1, columnspan=1,
                padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                pady=10)

    def continue_click(_event=None):
        global diff_input
        global effort_input
        global hold_flag
        global perceptibility_input

        perceptibility_input = perceptibility.get("1.0", "end-1c")
        diff_input = diff_selected.get()
        effort_input = effort_selected.get()

        if diff_input != "Bitte auswählen" and effort_input != "Bitte auswählen":
            post_five.destroy()

    empty_label = tk.Label(post_five, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=7, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_five,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=8, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    post_five.bind("<F8>", continue_click)
    post_five.focus_set()

    post_five.mainloop()

    return diff_input, effort_input, perceptibility_input


def post_experiment_questionnaire_six():
    global participated_earlier_input
    global other_input
    global hold_flag

    post_six = tk.Tk()
    post_six.attributes("-fullscreen", True)
    post_six.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    post_six.title("Fast geschafft! (6/6)")

    participated_earlier = tk.Label(post_six, justify="left",
                                    text="Hast Du bereits an einem früheren Experiment dieser "
                                         "Versuchsreihe teilgenommen?",
                                    font=("Arial", demographics_font_size))
    participated_earlier.grid(row=3, column=1, columnspan=1,
                              padx=ctypes.windll.user32.GetSystemMetrics(
                                  1) // 1.75,
                              pady=25)
    participated_earlier_selected = tk.StringVar()
    participated_earlier_selected.set("Bitte auswählen")
    participated_earlier = tk.OptionMenu(post_six,
                                         participated_earlier_selected,
                                         "Ja",
                                         "Nein.")
    participated_earlier.config(font=("Arial", demographics_font_size))
    participated_earlier.grid(row=4, column=1, columnspan=1,
                              padx=ctypes.windll.user32.GetSystemMetrics(
                                  1) // 1.75,
                              pady=10)

    other_label = tk.Label(post_six, justify="left",
                           text="Möchtest Du uns sonst noch etwas zum Versuch mitteilen?",
                           font=("Arial", demographics_font_size))
    other_label.grid(row=5, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=25)
    other = tk.Text(post_six, height=5, width=60,
                    font=("Arial", demographics_font_size))
    other.grid(row=6, column=1, columnspan=1,
               padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75, pady=10)

    def continue_click(_event=None):
        global other_input
        global participated_earlier_input

        other_input = other.get("1.0", "end-1c")
        participated_earlier_input = participated_earlier_selected.get()

        post_six.destroy()

    empty_label = tk.Label(post_six, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=7, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=10)
    continue_button = tk.Button(post_six,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=8, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=10)

    post_six.bind("<F8>", continue_click)
    post_six.focus_set()

    post_six.mainloop()

    return other_input, participated_earlier_input


def display_endcard_part_one():
    endcard = tk.Tk()
    endcard.attributes("-fullscreen", True)
    endcard.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    endcard.title("Danke für Deine Teilnahme!")

    endcard_label = tk.Label(endcard, justify="left",
                             text="Das war's auch schon mit Teil 1! Vielen Dank für "
                                  "Deine Teilnahme.\n\n"
                                  "Wenn Du auf den unteren Button klickst, wird eine zip-Datei mit Deinen Daten erstellt.\n"
                                  "Unter Umständen kann dieser Vorgang einige Sekunden dauern, die Kommandozeile schließt\n"
                                  "sich danach automatisch.\n"
                                  "Die Datei befindet sich dann in dem Ordner, in den Du die Versuchsdatei\n"
                                  "entpackt hast. Die zip-Datei fängt mit \"ERGEBNISSE_1_\" an, gefolgt vom\n"
                                  "momentanen Datum. Eine beispielhafte zip-Datei wäre:\n\n"
                                  "ERGEBNISSE_1_2021-04-06-14-41.zip (Datum und Uhrzeit variieren natürlich)\n\n"
                                  "Nachdem Du auf den unteren Button geklickt hast, sollte sich eine vorformulierte\n"
                                  "Email in Deinem Email-Client öffnen. Hänge Deine Ergebnisse vom ersten Teil bitte\n"
                                  "an diese Email an. \n"
                                  "Sende die zip-Datei bitte an die folgende Emailadresse (Abgabefrist: siehe BITTE_LESEN.pdf):\n\n"
                                  "versuche-psy3-oh@uni-wuerzburg.de\n\n"
                                  "Schicke die Email mit Deinen Daten aus Teil 1 am besten direkt ab, damit sie nicht verloren gehen.\n\n"
                                  "Lösche die Daten am besten erst, wenn ihr Eingang auch bestätigt wurde.\n\n"
                                  "Teil 2 solltest Du zwischen 4 bis 48 Stunden nach Teil 1 absolvieren.\n\n"
                                  "Wie sehen uns in Teil 2, bis dann!"
                             ,
                             font=("Arial", demographics_font_size))
    endcard_label.grid(row=1, column=1, columnspan=1,
                       padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                       pady=10)

    def continue_click(_event=None):
        global hold_flag

        hold_flag = False
        endcard.destroy()

    empty_label = tk.Label(endcard, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=2, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=5)
    continue_button = tk.Button(endcard,
                                text="Hier klicken um fortzufahren\n(oder F8 drücken)",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=3, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=5)

    endcard.bind("<F8>", continue_click)
    endcard.focus_set()

    endcard.mainloop()

    return hold_flag


def display_endcard_part_two():
    endcard = tk.Tk()
    endcard.attributes("-fullscreen", True)
    endcard.geometry(
        str(ctypes.windll.user32.GetSystemMetrics(0) // 2) + "x" + str(
            int(ctypes.windll.user32.GetSystemMetrics(1) // 1.5)))
    endcard.title("Danke für Deine Teilnahme!")

    endcard_label = tk.Label(endcard, justify="left",
                             text="Vielen Dank für Deine Teilnahme!\n\n"
                                  "Bitte klicke auf den unteren Button und melde Dich bei der Versuchsleitung.\n\n"
                                  "Nachdem Deine Daten ausgewertet und veröffentlicht wurden, wirst Du eine\n\n"
                                  "Aufklärung über die Hintergründe des Versuchs erhalten. Bis bald!\n\n ",
                             font=("Arial", demographics_font_size))
    endcard_label.grid(row=1, column=1, columnspan=1,
                       padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                       pady=10)

    def continue_click(_event=None):
        global hold_flag

        hold_flag = False

        endcard.destroy()

    empty_label = tk.Label(endcard, justify="left", text="",
                           font=("Arial", demographics_font_size))
    empty_label.grid(row=2, column=1, columnspan=1,
                     padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                     pady=5)
    continue_button = tk.Button(endcard,
                                text="Hier klicken (oder F8 drücken),\num Versuch zu beenden und zip-Datei zu erstellen",
                                pady=20, command=continue_click,
                                font=("Arial", demographics_font_size))
    continue_button.grid(row=3, column=1, columnspan=1,
                         padx=ctypes.windll.user32.GetSystemMetrics(1) // 1.75,
                         pady=5)

    endcard.bind("<F8>", continue_click)
    endcard.focus_set()

    endcard.mainloop()

    return hold_flag


def run_post_experiment_questionnaires(part_id, total_score, total_falls,
                                       total_eaten):
    global hold_flag
    global strategy_input
    global strategy_effort_input
    global delayedPerc_input
    global regularities_input
    global hypothesis_input
    global perceptibility_input
    global other_input
    global effort_input

    hypothesis_input = post_experiment_questionnaire_one(str(total_score),
                                                         str(total_falls),
                                                         str(total_eaten))
    regularities_input = post_experiment_questionnaire_two()

    strategy_input, strategy_effort_input, delayedPerc_input = \
        post_experiment_questionnaire_three()

    diff_input, effort_input, perceptibility_input = post_experiment_questionnaire_five()

    other_input, participated_earlier_input = post_experiment_questionnaire_six()

    hold_flag = display_endcard_part_two()

    return (
        hypothesis_input, regularities_input, strategy_input,
        strategy_effort_input,
        delayedPerc_input,
        diff_input, effort_input,
        perceptibility_input,
        hold_flag, other_input, participated_earlier_input)
