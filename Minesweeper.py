"""
Minesweeper - V1.1
Made By Nuker
"""

import tkinter as tk
from random import *
import sys


class Frame:
    def __init__(self, s, width=800, height=600):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(master=self.window, width=width, height=height)
        self.canvas.pack()
        self.g = []
        self.update_pos = []
        self.size = s
        self.fin = False
        self.first = True
        self._x = int()
        self._y = int()
        self.flags = int()

    def generate(self, _x=0, _y=0):
        self.canvas.delete('all')
        grid = []
        for i in range(count):
            grid.append([])
            for j in range(count):
                grid[i].append('')

        for i in range(count):
            for j in range(count):
                x = j * size + X
                y = i * size + Y
                grid[i][j] = Mine(x, y, size, canvas_1, x_no=j, y_no=i, g=grid)
        self.g = grid
        self.fin = False

        rand_list = []
        for i in range(len(grid)):
            for j in grid[i]:
                rand_list.append(j)
        rand_list.remove(self.g[_y][_x])
        for i in range(mines):
            mine_rand = randrange(len(rand_list))
            rand_list[mine_rand].mine = 1
            rand_list[mine_rand].stat = 'M'
            rand_list.pop(mine_rand)

        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                self.g[i][j].assign()
        self.background(mines)
        self.do_one_frame()

    def background(self, m):
        self.canvas.create_rectangle(380, 5, 420, 35, fill='white')
        self.canvas.create_text(400, 20, text=m)

    def finish(self, con='lose'):
        if self.fin is False:
            for i in range(len(self.g)):
                for j in range(len(self.g[i])):
                    if self.g[i][j].flag is True:
                        self.g[i][j].flag_rem()
                        self.g[i][j].flag = False
            for i in range(len(self.g)):
                for j in range(len(self.g[i])):
                    self.g[i][j].show(0)
            if con == 'lose':
                self.fin = True
                self.canvas.create_text(400, 300, text='You Lost', font='arial_black 50 bold')
            if con == 'win':
                self.fin = True
                self.canvas.create_text(400, 300, text='You Win', font='arial_black 50 bold')
            self.first = True

    def do_one_frame(self, pos=None, stat=None):
            if stat is None:
                stat = 'red'
            if stat == 0 or stat is True:
                self.g[pos[0]][pos[1]].mine_s(stat)
            elif pos is None:
                for i in self.g:
                    for j in i:
                        j.clear()
            elif len(pos) == 2:
                self.g[pos[0]][pos[1]].clear(stat)

    def motion(self, x):
        pass

    def click(self, click):
        if click.type == '4':
            if self.first is True or self.fin is True:
                self._x = int((click.x - 150) // self.size)
                self._y = int((click.y - 50) // self.size)
                self.generate(_x=int((click.x - 150) // self.size), _y=int((click.y - 50) // self.size))
                if not (self._x < 0 or self._x > count-1 or self._y < 0 or self._y > count-1) and \
                        self.g[self._y][self._x].flag is False:
                    if self.g[self._y][self._x].shown is False:
                        if self._x == int((click.x-150) // self.size) and self._y == int((click.y-50) // self.size):
                            self.do_one_frame([self._y, self._x], True)
                            # self.g[self._y][self._x].shown = True
            self.first = False
        if click.type == '4':
            self._x = int((click.x-150) // self.size)
            self._y = int((click.y-50) // self.size)
            if not (self._x < 0 or self._x > count-1 or self._y < 0 or self._y > count-1) and \
                    self.g[self._y][self._x].flag is False:
                if self.g[self._y][self._x].shown is False:
                    self.do_one_frame([self._y, self._x], 'blue')
        elif click.type == '5':
            if not (self._x < 0 or self._x > count-1 or self._y < 0 or self._y > count-1) and \
                    self.g[self._y][self._x].flag is False:
                if self.g[self._y][self._x].shown is False:
                    if self._x == int((click.x-150) // self.size) and self._y == int((click.y-50) // self.size):
                        self.do_one_frame([self._y, self._x], 0)
                    else:
                        self.do_one_frame([self._y, self._x], 'red')
            loop = 0
            for i in range(len(self.g)):
                for j in range(len(self.g[i])):
                    if self.g[i][j].shown is True and not self.g[i][j].stat == 'M':
                        loop += 1
            if loop == (count ** 2) - mines:
                self.finish('win')

    def flag(self, event):
        self._x = int((event.x-150) // self.size)
        self._y = int((event.y-50) // self.size)
        flags = 0
        if self.g[self._y][self._x].flag is False and self.g[self._y][self._x].shown is False:
            self.g[self._y][self._x].flag_draw()
            self.g[self._y][self._x].flag = True
        elif self.g[self._y][self._x].flag is True and self.g[self._y][self._x].shown is False:
            self.g[self._y][self._x].flag_rem()
            self.g[self._y][self._x].flag = False

        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if self.g[i][j].flag is True:
                    flags += 1
        self.flags = flags
        self.background(mines-self.flags)


class Mine:
    def __init__(self, x=0.0, y=0.0, size_f=1.0, par=None, x_no=0, y_no=0, g=None):
        self.canvas = par.canvas
        self.canvas.create_rectangle(x, y, x + size_f, y + size_f)
        self.size = size_f
        self.mine = 0
        self.code = None
        self.x = x
        self.y = y
        self.xNo = x_no
        self.yNo = y_no
        self.shown = False
        self.g = g
        self.stat = None
        self.flag = False

    def clear(self, fill='red'):
        self.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, fill=fill)

    def flag_draw(self):
        self.clear('pink')
        self.canvas.create_text(self.x + size / 2, self.y + size / 2, text='F',
                                font='arial_black {} bold'.format(int(size // 2)))

    def flag_rem(self):
        self.clear('red')

    def assign(self):
        n = 0
        ly = self.yNo - 1
        lx = self.xNo - 1
        if self.mine == 1:
            self.stat = 'M'
        else:
            for i in range(3):
                for j in range(3):
                    if not (i + ly < 0 or i + ly > count-1 or j + lx < 0 or j + lx > count-1):
                        test = self.g[i + ly][j + lx]
                        if test.mine == 1:
                            n += 1
            self.stat = n

    def mine_s(self, f=False):
        n = 0
        ly = self.yNo-1
        lx = self.xNo-1
        if self.stat == 'M':
            self.show()
            canvas_1.finish()
        if self.shown is False:
            for i in range(3):
                for j in range(3):
                    if not (i + ly < 0 or i + ly > count-1 or j + lx < 0 or j + lx > count-1):
                        if self.stat == 0:
                            self.show()
                            self.g[i + ly][j + lx].mine_s()
                        elif self.g[i + ly][j + lx].stat == 0 and f is True:
                            self.show()
                            self.g[i + ly][j + lx].mine_s()
                        else:
                            self.show()
        return n

    def show(self, r=1):
        if r == 1:
            canvas_1.canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill='gray')
        if self.stat != 0:
            canvas_1.canvas.create_text(self.x+size/2, self.y+size/2, text=self.stat,
                                        font="arial_black {} bold".format(int(size//2)))
        self.shown = True


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    mines_init = 'auto'
    count = 30
    if mines_init == 'auto':
        mines = int(count**2/10)
    else:
        mines = mines_init
    size = 500/count
    X, Y = (800-count*size)/2, 50

    canvas_1 = Frame(size)
    canvas_1.generate()
    canvas_1.background(mines)

    canvas_1.do_one_frame()
    canvas_1.window.bind('<Motion>', canvas_1.motion)
    canvas_1.window.bind('<Button-1>', canvas_1.click)
    canvas_1.window.bind('<ButtonRelease-1>', canvas_1.click)
    canvas_1.window.bind('<Button-3>', canvas_1.flag)
    canvas_1.window.mainloop()
