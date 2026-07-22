# ftp_python.py — двухпанельный FTP-клиент на Python

import ftplib
import os
import curses
import time
import threading
from datetime import datetime

class FTPClient:
    def __init__(self):
        self.ftp = None
        self.local_path = os.getcwd()
        self.remote_path = "/"
        self.local_files = []
        self.remote_files = []
        self.running = True

    def connect(self, host, user='', password='', port=21):
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(host, port)
            self.ftp.login(user, password)
            self.remote_path = "/"
            return True
        except Exception as e:
            return False

    def list_local(self):
        try:
            items = os.listdir(self.local_path)
            self.local_files = sorted(items)
        except:
            self.local_files = []

    def list_remote(self):
        try:
            items = self.ftp.nlst()
            self.remote_files = sorted(items)
        except:
            self.remote_files = []

    def upload(self, filename):
        try:
            local_file = os.path.join(self.local_path, filename)
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {filename}', f)
            return True
        except:
            return False

    def download(self, filename):
        try:
            with open(os.path.join(self.local_path, filename), 'wb') as f:
                self.ftp.retrbinary(f'RETR {filename}', f.write)
            return True
        except:
            return False

    def delete_remote(self, filename):
        try:
            self.ftp.delete(filename)
            return True
        except:
            return False

    def delete_local(self, filename):
        try:
            os.remove(os.path.join(self.local_path, filename))
            return True
        except:
            return False

    def mkdir_remote(self, dirname):
        try:
            self.ftp.mkd(dirname)
            return True
        except:
            return False

    def mkdir_local(self, dirname):
        try:
            os.mkdir(os.path.join(self.local_path, dirname))
            return True
        except:
            return False

    def rename_remote(self, old, new):
        try:
            self.ftp.rename(old, new)
            return True
        except:
            return False

    def rename_local(self, old, new):
        try:
            os.rename(os.path.join(self.local_path, old), os.path.join(self.local_path, new))
            return True
        except:
            return False

def draw_panel(stdscr, y, x, height, width, title, items, cursor_pos, is_local):
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(y, x, f" {title} ".center(width, ' '))
    stdscr.attroff(curses.A_REVERSE)
    y += 1
    for i, item in enumerate(items):
        if i == cursor_pos:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(y+i, x, item[:width-1])
        stdscr.attroff(curses.A_REVERSE)
    # очищаем остальное
    for i in range(len(items), height-2):
        stdscr.addstr(y+i, x, " " * (width-1))

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    panel_width = width // 2 - 2
    panel_height = height - 8

    client = FTPClient()
    # Подключение (для теста используем публичный FTP)
    host = "test.rebex.net"
    user = "demo"
    password = "password"
    if not client.connect(host, user, password):
        stdscr.addstr(0, 0, "Ошибка подключения", curses.A_BOLD)
        stdscr.refresh()
        time.sleep(2)
        return

    local_pos = 0
    remote_pos = 0
    running = True
    while running:
        client.list_local()
        client.list_remote()
        stdscr.clear()
        # Заголовок
        stdscr.addstr(0, 0, f"FTPCommander (Python) - {host}", curses.A_BOLD)
        stdscr.addstr(1, 0, "Локальная: " + client.local_path)
        stdscr.addstr(1, panel_width+3, "Удалённая: " + client.remote_path)

        # Панели
        draw_panel(stdscr, 2, 0, panel_height, panel_width,
                   "Локальная", client.local_files, local_pos, True)
        draw_panel(stdscr, 2, panel_width+3, panel_height, panel_width,
                   "Удалённая", client.remote_files, remote_pos, False)

        # Подсказки
        hints = "F1-Помощь F5-Копировать F6-Переместить F7-Папка F8-Удалить F10-Выход"
        stdscr.addstr(height-3, 0, hints, curses.A_DIM)

        # Ввод команд
        stdscr.addstr(height-2, 0, "> ")
        cmd = stdscr.getstr().decode('utf-8').strip()
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0] == 'q' or parts[0] == 'exit':
            break
        elif parts[0] == 'cd' and len(parts) > 1:
            try:
                os.chdir(parts[1])
                client.local_path = os.getcwd()
            except:
                pass
        elif parts[0] == 'cdr' and len(parts) > 1:
            try:
                client.ftp.cwd(parts[1])
                client.remote_path = client.ftp.pwd()
            except:
                pass
        elif parts[0] == 'get' and len(parts) > 1:
            if client.download(parts[1]):
                stdscr.addstr(height-1, 0, "Скачано")
            else:
                stdscr.addstr(height-1, 0, "Ошибка скачивания")
        elif parts[0] == 'put' and len(parts) > 1:
            if client.upload(parts[1]):
                stdscr.addstr(height-1, 0, "Загружено")
            else:
                stdscr.addstr(height-1, 0, "Ошибка загрузки")
        elif parts[0] == 'del' and len(parts) > 1:
            # удаление на удалённой стороне
            if client.delete_remote(parts[1]):
                stdscr.addstr(height-1, 0, "Удалено")
            else:
                stdscr.addstr(height-1, 0, "Ошибка удаления")
        elif parts[0] == 'dello' and len(parts) > 1:
            if client.delete_local(parts[1]):
                stdscr.addstr(height-1, 0, "Удалено локально")
            else:
                stdscr.addstr(height-1, 0, "Ошибка удаления")
        elif parts[0] == 'mkdir' and len(parts) > 1:
            if client.mkdir_remote(parts[1]):
                stdscr.addstr(height-1, 0, "Папка создана")
            else:
                stdscr.addstr(height-1, 0, "Ошибка создания")
        elif parts[0] == 'mkdir_local' and len(parts) > 1:
            if client.mkdir_local(parts[1]):
                stdscr.addstr(height-1, 0, "Папка создана локально")
            else:
                stdscr.addstr(height-1, 0, "Ошибка создания")
        elif parts[0] == 'help':
            stdscr.addstr(height-1, 0, "Команды: cd, cdr, get, put, del, dello, mkdir, mkdir_local, q")
        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
