// ftp_rs.rs — двухпанельный FTP-клиент на Rust (ftp crate)

use ftp::FtpStream;
use std::io::{self, Write, BufRead};
use std::fs;
use std::path::Path;
use std::time::Duration;

fn main() {
    let mut ftp = FtpStream::connect("test.rebex.net:21").unwrap();
    let _ = ftp.login("demo", "password").unwrap();
    let mut local_path = ".".to_string();
    let mut remote_path = "/".to_string();

    let stdin = io::stdin();
    let mut reader = stdin.lock();
    loop {
        let local_files = list_local(&local_path);
        let remote_files = list_remote(&mut ftp);
        print_panel(&local_path, &remote_path, &local_files, &remote_files);
        print!("> ");
        io::stdout().flush().unwrap();
        let mut cmd = String::new();
        if reader.read_line(&mut cmd).is_err() { break; }
        let cmd = cmd.trim();
        if cmd == "q" || cmd == "exit" { break; }
        else if cmd.starts_with("cd ") {
            let dir = &cmd[3..];
            let new_path = Path::new(&local_path).join(dir);
            if new_path.is_dir() {
                local_path = new_path.to_string_lossy().to_string();
            }
        } else if cmd.starts_with("cdr ") {
            let dir = &cmd[4..];
            if let Ok(()) = ftp.cwd(dir) {
                remote_path = ftp.pwd().unwrap_or("/".to_string());
            }
        } else if cmd.starts_with("get ") {
            let file = &cmd[4..];
            download(&mut ftp, file, &local_path);
        } else if cmd.starts_with("put ") {
            let file = &cmd[4..];
            upload(&mut ftp, file, &local_path);
        }
    }
    let _ = ftp.quit();
}

fn list_local(path: &str) -> Vec<String> {
    let mut files = Vec::new();
    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries.flatten() {
            if let Ok(name) = entry.file_name().into_string() {
                files.push(name);
            }
        }
    }
    files.sort();
    files
}

fn list_remote(ftp: &mut FtpStream) -> Vec<String> {
    let mut files = Vec::new();
    if let Ok(list) = ftp.nlst(Some(".")) {
        for name in list {
            files.push(name);
        }
    }
    files.sort();
    files
}

fn print_panel(local: &str, remote: &str, local_files: &[String], remote_files: &[String]) {
    println!("FTPCommander (Rust) - test.rebex.net");
    println!("Локальная: {}", local);
    println!("Удалённая: {}", remote);
    println!("--- Локальная ---");
    for f in local_files.iter().take(10) {
        println!("{}", f);
    }
    println!("--- Удалённая ---");
    for f in remote_files.iter().take(10) {
        println!("{}", f);
    }
    println!("Команды: cd, cdr, get, put, q");
}

fn download(ftp: &mut FtpStream, file: &str, local_path: &str) {
    if let Ok(mut data) = ftp.retr(file) {
        let mut buf = Vec::new();
        if let Ok(_) = data.read_to_end(&mut buf) {
            let local_file = Path::new(local_path).join(file);
            if let Ok(_) = fs::write(&local_file, buf) {
                println!("Скачано: {}", file);
            }
        }
    }
}

fn upload(ftp: &mut FtpStream, file: &str, local_path: &str) {
    let local_file = Path::new(local_path).join(file);
    if let Ok(data) = fs::read(&local_file) {
        if let Ok(()) = ftp.put(file, &data[..]) {
            println!("Загружено: {}", file);
        }
    }
}
