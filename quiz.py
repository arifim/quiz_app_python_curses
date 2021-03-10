#!/usr/bin/python3

# 🎄🌲🎄

import curses
from curses import textpad
import time
import json


with open("questions.json", "r") as file:
    data = json.load(file)

stdsrc = curses.initscr()
h, w = stdsrc.getmaxyx()

def print_question(q, selected_answer="", style=0):
    
    question = q["Question"]
    x = 20
    y = 5
    stdsrc.attron(curses.color_pair(1))
    stdsrc.addstr(y, x, question)
    stdsrc.attroff(curses.color_pair(1))
    answers = q["Answers"]

    for ch, answer in zip("ABCD", answers):
        y += 2
        if ch in selected_answer:
            stdsrc.attron(curses.color_pair(style))
            stdsrc.addstr(y, x+1, answer)
            stdsrc.attroff(curses.color_pair(style))
        else:
            stdsrc.addstr(y, x+1, answer)


def show_correct_answers(q, correct_answers, user_answers):

    question = q["Question"];
    x = 20
    y = 5
    stdsrc.attron(curses.color_pair(1))
    stdsrc.addstr(y, x, question)
    stdsrc.attroff(curses.color_pair(1))
    answers = q["Answers"]

    for ch, answer in zip("ABCD", answers):
        y += 2
        # All answers are true
        if ch in correct_answers and ch in user_answers:
            stdsrc.attron(curses.color_pair(2))
            stdsrc.addstr(y, x+1, "" + answer)
            stdsrc.attroff(curses.color_pair(2))
        elif ch in user_answers and ch not in correct_answers:
            stdsrc.attron(curses.color_pair(3))
            stdsrc.addstr(y, x+1, answer)
            stdsrc.attroff(curses.color_pair(3))
        elif ch in correct_answers:
            stdsrc.attron(curses.color_pair(2))
            stdsrc.addstr(y, x+1, answer)
            stdsrc.attroff(curses.color_pair(2)) 
        else:
            stdsrc.addstr(y, x+1, answer)

def check_answers(user_answers, correct_answers):
    if len(user_answers) != len(correct_answers):
        return False
        
    for answer in user_answers:
        if answer not in correct_answers:
            return False
    return True 

def main(stdsrc):
    curses.start_color()
    # Disabling the cursor
    curses.curs_set(0) 

    # setting font color and background color
    # <1> is the number of a color pair
    # <COLOR_GREEN> is font color
    # <COLOR_YELLOW> is background color
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)


    current_question_index = 0
    selected = False
    selected_answer = ""
    score = 0
    while True:
        stdsrc.clear()
        curses.flushinp()
        q = data["Questions"][current_question_index]
        stdsrc.addstr(0, 0, f"Qestion {current_question_index+1} of {len(q)}")
        if selected:
            print_question(q, selected_answer=selected_answer, style=2)
        else:
            print_question(q, selected_answer=selected_answer)

        key = stdsrc.getch()
        if key == 97:
            selected = True
            if "A" in selected_answer:
                selected_answer = selected_answer.replace("A", "")
            else:
                selected_answer += "A"
        elif key == 98:
            selected = True
            if "B" in selected_answer:
                selected_answer = selected_answer.replace("B", "")
            else:
                selected_answer += "B" 
        elif key == 99:
            selected = True
            if "C" in selected_answer:
                selected_answer = selected_answer.replace("C", "")
            else:
                selected_answer += "C"
        elif key == 100:
            selected = True
            if "D" in selected_answer:
                selected_answer = selected_answer.replace("D", "")
            else:
                selected_answer += "D"

        elif key == ord('q'): # ESC Key
            s = "Are you sure you want to finish quiz? (Y/N)"
            stdsrc.clear()
            stdsrc.addstr(h//2-10, w//2 - len(s)//2, s)
            stdsrc.refresh()
            k = stdsrc.getch()
            if k == ord("Y") or k == ord("y"):
                break
            else:
                pass

        elif key == curses.KEY_ENTER or key in [10, 13]:
            correct_answers = q["Correct_answer"]
            current_question_index += 1

            if check_answers(selected_answer, correct_answers):
                score += 1

            show_correct_answers(q, correct_answers, selected_answer)
            stdsrc.refresh()
            time.sleep(2)

            if current_question_index >= len(data["Questions"]): 
                break

            selected = False
            selected_answer = ""
    
        stdsrc.refresh()
    
    stdsrc.clear()
    
    result_str = "You score is " + str(100 // len(data["Questions"]) * score) + "%"
    stdsrc.attron(curses.color_pair(1)) 
    textpad.rectangle(stdsrc, h//2-11, w//2-len(result_str)//2-1, h//2-9, w//2 + len(result_str)//2+1)
    stdsrc.addstr(h//2-10, w//2 - len(result_str)//2, result_str)
    stdsrc.attroff(curses.color_pair(1))
    stdsrc.refresh()

    time.sleep(3)
    stdsrc.clear()
    stdsrc.refresh()


curses.wrapper(main)


