// ftp_go.go — двухпанельный FTP-клиент на Go (github.com/jlaffaye/ftp)

package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
	"github.com/jlaffaye/ftp"
)

var client *ftp.ServerConn
var localPath = "."
var remotePath = "/"
var localFiles []string
var remoteFiles []string

func main() {
	var err error
	client, err = ftp.Dial("test.rebex.net:21")
	if err != nil {
		fmt.Println("Ошибка подключения:", err)
		return
	}
	err = client.Login("demo", "password")
	if err != nil {
		fmt.Println("Ошибка логина:", err)
		return
	}
	scanner := bufio.NewScanner(os.Stdin)
	for {
		listLocal()
		listRemote()
		printPanel()
		fmt.Print("> ")
		if !scanner.Scan() {
			break
		}
		cmd := strings.TrimSpace(scanner.Text())
		if cmd == "q" || cmd == "exit" {
			break
		} else if strings.HasPrefix(cmd, "cd ") {
			dir := strings.TrimPrefix(cmd, "cd ")
			newPath := filepath.Join(localPath, dir)
			if info, err := os.Stat(newPath); err == nil && info.IsDir() {
				localPath = newPath
			}
		} else if strings.HasPrefix(cmd, "cdr ") {
			dir := strings.TrimPrefix(cmd, "cdr ")
			if err := client.ChangeDir(dir); err == nil {
				remotePath = "/" + dir
			}
		} else if strings.HasPrefix(cmd, "get ") {
			file := strings.TrimPrefix(cmd, "get ")
			download(file)
		} else if strings.HasPrefix(cmd, "put ") {
			file := strings.TrimPrefix(cmd, "put ")
			upload(file)
		}
	}
	client.Quit()
}

func listLocal() {
	localFiles = nil
	files, _ := os.ReadDir(localPath)
	for _, f := range files {
		localFiles = append(localFiles, f.Name())
	}
}

func listRemote() {
	remoteFiles = nil
	entries, _ := client.List(".")
	for _, e := range entries {
		remoteFiles = append(remoteFiles, e.Name)
	}
}

func printPanel() {
	fmt.Println("FTPCommander (Go) - test.rebex.net")
	fmt.Println("Локальная:", localPath)
	fmt.Println("Удалённая:", remotePath)
	fmt.Println("--- Локальная ---")
	for i, f := range localFiles {
		if i >= 10 {
			break
		}
		fmt.Println(f)
	}
	fmt.Println("--- Удалённая ---")
	for i, f := range remoteFiles {
		if i >= 10 {
			break
		}
		fmt.Println(f)
	}
	fmt.Println("Команды: cd, cdr, get, put, q")
}

func download(file string) {
	r, err := client.Retr(file)
	if err != nil {
		fmt.Println("Ошибка скачивания:", err)
		return
	}
	defer r.Close()
	f, err := os.Create(filepath.Join(localPath, file))
	if err != nil {
		fmt.Println("Ошибка создания файла:", err)
		return
	}
	defer f.Close()
	io.Copy(f, r)
	fmt.Println("Скачано:", file)
}

func upload(file string) {
	f, err := os.Open(filepath.Join(localPath, file))
	if err != nil {
		fmt.Println("Ошибка открытия файла:", err)
		return
	}
	defer f.Close()
	err = client.Stor(file, f)
	if err != nil {
		fmt.Println("Ошибка загрузки:", err)
	} else {
		fmt.Println("Загружено:", file)
	}
}
