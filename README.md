📁 FTPCommander — двухпанельный FTP-клиент
Мощный двухпанельный FTP-клиент для удобной работы с удалёнными файлами.
Поддерживает локальную и удалённую навигацию, загрузку/скачивание, удаление, переименование, создание папок и многое другое.
Реализован на 7 языках программирования для демонстрации различных подходов к созданию сетевых приложений.

https://img.shields.io/github/repo-size/yourname/ftpcommander
https://img.shields.io/github/stars/yourname/ftpcommander?style=social
https://img.shields.io/badge/License-MIT-blue.svg

🧠 Концепция
FTPCommander — это клиент FTP с интерфейсом в стиле «две панели» (как в Midnight Commander). Он позволяет:

✅ Подключаться к FTP-серверам с поддержкой анонимного доступа и авторизации.

✅ Навигировать по локальной и удалённой файловой системе.

✅ Копировать файлы и папки между панелями (загрузка/скачивание).

✅ Удалять, переименовывать и создавать папки.

✅ Отображать содержимое панелей в виде списка.

✅ Поддерживать активный и пассивный режимы.

✅ Работать как в консоли (с цветным выводом), так и в GUI.

✅ Быть простым и интуитивно понятным.

🚀 Как запустить
Для каждой версии требуются соответствующие библиотеки. Инструкции по установке и запуску приведены ниже.

Python
bash
pip install ftplib  # встроен
python ftp_python.py
C++
bash
# Требуется libcurl (sudo apt install libcurl4-openssl-dev) и ncurses (sudo apt install libncurses-dev)
g++ -std=c++17 ftp_cpp.cpp -o ftp -lcurl -lncurses
./ftp
Java
bash
# Требуется Apache Commons Net (скачать commons-net.jar)
javac -cp .:commons-net.jar ftp_java.java
java -cp .:commons-net.jar ftp_java
C# (.NET Core)
bash
dotnet add package FluentFTP
dotnet run
Go
bash
go get github.com/jlaffaye/ftp
go run ftp_go.go
Rust
bash
cargo add ftp
cargo build --release && ./target/release/ftp_rs
JavaScript (Node.js)
bash
npm install basic-ftp
node ftp_js.js
🧩 Пример сессии (консоль)
text
+--------------------------------------------------+
| FTPCommander v2.0                                 |
| Локальная: /home/user                Удалённая: /  |
| [..]                              [..]            |
| file1.txt                         pub/            |
| file2.jpg                         incoming/       |
| folder/                           README.md       |
|                                                   |
| F1-Помощь  F5-Копировать  F6-Переместить  F7-Папка|
| F8-Удалить  F10-Выход                            |
+--------------------------------------------------+
📦 Содержимое репозитория
Файл	Язык	Особенности
ftp_python.py	Python	ftplib + curses (консольный GUI)
ftp_cpp.cpp	C++	libcurl + ncurses, цветной вывод
ftp_java.java	Java	Apache Commons Net, текстовый интерфейс
ftp_cs.cs	C#	FluentFTP, консольный двухпанельный
ftp_go.go	Go	goftp, горутины для асинхронности
ftp_rs.rs	Rust	ftp crate, termion, цветной вывод
ftp_js.js	JavaScript	basic-ftp, интерактивный CLI
🔮 Расширенные функции
Поддержка SFTP (в планах).

Закладки для быстрого доступа.

Фоновые операции (загрузка/скачивание в фоне).

📜 Лицензия
MIT — свободно используйте, модифицируйте и распространяйте.

🤝 Вклад
Приветствуются пул-реквесты с улучшениями, поддержкой новых протоколов и расширением функциональности.

⭐ Если проект помогает вам управлять файлами — поставьте звёздочку!
