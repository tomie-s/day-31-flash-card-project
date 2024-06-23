from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
timer = None


# ---------------------------- TIMER ------------------------------- #
def count_down(count):
    global timer
    canvas.itemconfig(card_timer, text=f'{count}')

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        window.after_cancel(timer)
        canvas.itemconfig(card_timer, text='Did you get it right?', fill='white', font=(FONT_NAME, 26, 'italic'))


# ---------------------------- SHOW NEW WORD ------------------------------- #
current_card = {}
word_list = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    primary_data = pandas.read_csv('data/french_words.csv')
    word_list = primary_data.to_dict(orient="records")
else:
    word_list = data.to_dict(orient="records")


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(word_list)

    canvas.itemconfig(card_bg, image=card_front_img)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_timer, text='', font=(FONT_NAME, 36, 'bold'), fill='black')

    count_down(3)
    flip_timer = window.after(3000, flip_card)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    canvas.itemconfig(card_bg, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')


# ---------------------------- UPDATE WORD LIST ------------------------------- #
def word_known():
    word_list.remove(current_card)

    new_data = pandas.DataFrame(word_list)
    new_data.to_csv('data/words_to_learn.csv', index=False)

    next_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
card_bg = canvas.create_image(401, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text='', font=(FONT_NAME, 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=(FONT_NAME, 60, 'bold'))
card_timer = canvas.create_text(400, 420, text='', font=(FONT_NAME, 36, 'bold'))

canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_btn_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_btn_img, highlightthickness=0, borderwidth=0, command=next_word)
wrong_button.grid(column=0, row=1)

right_btn_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_btn_img, highlightthickness=0, borderwidth=0, command=word_known)
right_button.grid(column=1, row=1)

# Display first word on program launch
next_word()

window.mainloop()
