// ftp_cpp.cpp — двухпанельный FTP-клиент на C++ (libcurl + ncurses)

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <curl/curl.h>
#include <ncurses.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>

using namespace std;

// Глобальные переменные для FTP
CURL *curl;
string remote_path = "/";
string local_path = ".";
vector<string> local_files, remote_files;

// Callback для записи данных
size_t write_data(void *ptr, size_t size, size_t nmemb, string *data) {
    data->append((char*)ptr, size * nmemb);
    return size * nmemb;
}

// Получение списка файлов (упрощённо)
bool list_remote() {
    remote_files.clear();
    string response;
    CURLcode res;
    string url = "ftp://" + string("test.rebex.net") + remote_path;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
    curl_easy_setopt(curl, CURLOPT_USERPWD, "demo:password");
    res = curl_easy_perform(curl);
    if (res != CURLE_OK) return false;
    // Парсинг ответа (очень упрощённо)
    string line;
    size_t pos = 0;
    while ((pos = response.find('\n')) != string::npos) {
        line = response.substr(0, pos);
        response.erase(0, pos+1);
        if (line.empty()) continue;
        // Имя файла — последнее слово
        size_t last = line.find_last_of(' ');
        if (last != string::npos) {
            string name = line.substr(last+1);
            if (!name.empty() && name != "." && name != "..") {
                remote_files.push_back(name);
            }
        }
    }
    return true;
}

void list_local() {
    local_files.clear();
    DIR *dir = opendir(local_path.c_str());
    if (!dir) return;
    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
        string name = ent->d_name;
        if (name != "." && name != "..") {
            local_files.push_back(name);
        }
    }
    closedir(dir);
}

void draw_panel(WINDOW *win, int y, int x, int height, int width, const string& title,
                const vector<string>& items, int cursor) {
    wattron(win, A_REVERSE);
    mvwprintw(win, y, x, " %s ", title.c_str());
    wattroff(win, A_REVERSE);
    for (int i=0; i<height-2 && i<items.size(); ++i) {
        if (i == cursor) wattron(win, A_REVERSE);
        mvwprintw(win, y+1+i, x, "%-*s", width-1, items[i].c_str());
        wattroff(win, A_REVERSE);
    }
}

int main() {
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (!curl) {
        cerr << "Ошибка инициализации curl" << endl;
        return 1;
    }

    initscr();
    keypad(stdscr, TRUE);
    curs_set(0);
    int height, width;
    getmaxyx(stdscr, height, width);
    int panel_w = width / 2 - 2;
    int panel_h = height - 6;

    // Подключение (тест)
    list_remote();

    int local_pos=0, remote_pos=0;
    string cmd;
    while (true) {
        clear();
        list_local();
        list_remote();

        // Заголовок
        mvprintw(0, 0, "FTPCommander (C++) - test.rebex.net");
        mvprintw(1, 0, "Локальная: %s", local_path.c_str());
        mvprintw(1, panel_w+3, "Удалённая: %s", remote_path.c_str());

        // Панели
        draw_panel(stdscr, 2, 0, panel_h, panel_w, "Локальная", local_files, local_pos);
        draw_panel(stdscr, 2, panel_w+3, panel_h, panel_w, "Удалённая", remote_files, remote_pos);

        mvprintw(height-3, 0, "F1-Помощь F5-Копировать F6-Переместить F7-Папка F8-Удалить F10-Выход");
        mvprintw(height-2, 0, "> ");
        refresh();

        char buf[100];
        echo();
        getstr(buf);
        noecho();
        cmd = buf;
        if (cmd == "q" || cmd == "exit") break;
        else if (cmd.rfind("cd ", 0) == 0) {
            string dir = cmd.substr(3);
            if (chdir(dir.c_str()) == 0) {
                char *cwd = getcwd(NULL, 0);
                local_path = cwd;
                free(cwd);
            }
        } else if (cmd.rfind("cdr ", 0) == 0) {
            string dir = cmd.substr(4);
            // упрощённо
        } else if (cmd.rfind("get ", 0) == 0) {
            // скачивание
        } else if (cmd.rfind("put ", 0) == 0) {
            // загрузка
        }
    }

    endwin();
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    return 0;
}
