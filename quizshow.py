#!/usr/bin/python
import curses
import yaml
import time
import os, sys

f = open('dino-jack.yml')
script = yaml.load(f)
f.close()

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

def display_video(file):
    os.system('omxplayer -b "%s" >/dev/null 2>&1' % file)

def display_image(file):
    os.spawnlp(os.P_WAIT, 'fbv', 'fbv', file)

players = []
player_stride = 0
script_index = 0
question_n = 1

window = curses.initscr()
curses.start_color()
h, w = window.getmaxyx()

# Initialize colors
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Question window
qwin = window.derwin(12, w - 10, 5, 5)
qwin.attrset(curses.color_pair(1) | curses.A_BOLD)
qwin_h, qwin_w = qwin.getmaxyx()

# Answers window
awin = window.derwin(8, w - 10, h - 13, 5)
awin.attrset(curses.color_pair(2))
awin_h, awin_w = awin.getmaxyx()

# Players window
pwin = window.derwin(3, w - 6, h - 4, 2)
pwin.attrset(curses.color_pair(3))
pwin_h, pwin_w = pwin.getmaxyx()

def wrap(text, w):
    r = []
    for line in text.split('\n'):
        i = 0
        l = len(line)
        if l == 0:
            r.append(line)
            continue
        while i < l:
            j = i + w
            if j >= l:
                r.append(line[i:])
                break
            else:
                while line[j] != ' ':
                    j -= 1
                r.append(line[i:j])
                i = j + 1
    return r

def display_question_q(item):
    qy = 0
    for line in wrap(item['q'], qwin_w):
        qx = 0
        for c in line:
            qwin.addstr(qy, qx, line[qx])
            qwin.refresh()
            qx += 1
            time.sleep(0.04)
        qy += 1

aletters = ['A', 'B', 'C', 'D']
def display_answers(item):
    ay = 0
    for answer in item['a']:
        awin.addstr(ay, 0, "%s)" % aletters[ay])
        awin.refresh()
        time.sleep(0.5)
        awin.addstr(ay, 3, answer)
        awin.refresh()
        time.sleep(1.0)
        ay += 1
    window.getch(h - 1, w - 1)
    ay = item['w']
    awin.chgat(ay, 0, 3 + len(item['a'][ay]), curses.A_REVERSE)
    awin.refresh()

    while True:
        to = window.getch(h - 1, w - 1)
        if chr(to) == 'x':
            break
        try:
            player = int(chr(to), 16) - 1
        except ValueError:
            continue
        points = 10
        if 'points' in item:
            points = int(item['points'])
        try:
            players[player].score += points
        except IndexError:
            continue
        break

def display_question(item, n=0):
    try:
        points = item['points']
    except KeyError:
        points = 10
    window.addstr(0, 0, "Question %d" % n, curses.color_pair(4))
    window.addstr(0, w - 10, "%3d points" % points, curses.color_pair(4))
    window.refresh()
    display_players()
    time.sleep(3)
    display_question_q(item)
    time.sleep(2)
    display_answers(item)
    display_players()
    window.getch()
    qwin.clear()
    qwin.refresh()
    awin.clear()
    awin.refresh()

def display_title(item):
    window.clear()
    head = item['title']['head']
    lines = item['title']['text'].split('\n')
    def put_line(y, str, attr=0):
        x = w / 2 - len(str) / 2
        window.addstr(y, x, str, attr)
        window.refresh()
    l = len(lines) + 2
    y = h / 2 - l / 2
    put_line(y, head, curses.A_BOLD)
    time.sleep(1)
    y += 2
    for l in lines:
        put_line(y, l)
        time.sleep(0.5)
        y += 1
    window.getch()
    window.clear()
    window.refresh()

def display_players():
    pwin.clear()
    px = 0
    py = 0
    c = 1
    for p in players:
        pwin.addstr(py, px, "%1X " % c)
        pwin.addstr("%-*s " % (player_stride, p.name), curses.A_BOLD)
        pwin.addstr("%3d" % p.score, curses.A_REVERSE)
        px += player_stride + 8
        if px >= pwin_w - 2:
            px = 0
            py += 1
        c += 1
    pwin.refresh()

def gather_players():
    global player_stride, players

    ok = False

    while not ok:
        window.clear()
        window.refresh()
        window.addstr(4, 5, "Add up to 15 players. Enter a blank line")
        window.addstr(5, 5, "to finish.")
        n = 1
        players = []
        name = "X"
        while name != '' and len(players) < 15:
            window.addstr(6 + n, 5, "Player %s's name: " % n)
            name = window.getstr()
            if len(name) > player_stride:
                player_stride = len(name)
            players.append(Player(name))
            n += 1
        if name == '':
            players.pop()
        display_players()
        window.addstr(7 + n, 5, "%s players. Is this correct? " % len(players))
        answer = window.getstr()
        if answer.lower() == 'y':
            ok = True

def save_state():
    state = dict(
        players = players,
        index = script_index,
        question = question_n
    )
    f = open('state.yml', 'w')
    yaml.dump(state, f)
    f.close()

def load_state(filename):
    global players, script_index, question_n
    f = open(filename)
    state = yaml.load(f)
    f.close()
    players = state['players']
    script_index = state['index']
    question_n = state['question']

def main():
    global script_index, question_n
    if len(sys.argv) > 1:
        load_state(sys.argv[1])
    else:
        gather_players()

    window.clear()
    window.refresh()
    curses.noecho()
    display_players()
    while script_index < len(script):
        save_state()
        item = script[script_index]
        if 'image' in item:
            display_image(item['image'])
        elif 'video' in item:
            display_video(item['video'])
        elif 'title' in item:
            display_title(item)
        elif 'q' in item:
            display_question(item, question_n)
            question_n += 1
        script_index += 1
    save_state()
    window.addstr(h / 2, w / 2 - 8, "G A M E   O V E R")
    window.getch()
    curses.endwin()

try:
    main()
except KeyboardInterrupt:
    pass

curses.endwin()
