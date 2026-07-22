// ftp_js.js — двухпанельный FTP-клиент на JavaScript (Node.js)

const { Client } = require('basic-ftp');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function main() {
    const client = new Client();
    client.ftp.verbose = true;
    try {
        await client.access({
            host: "test.rebex.net",
            user: "demo",
            password: "password",
            secure: false
        });
    } catch (err) {
        console.log("Ошибка подключения:", err.message);
        return;
    }

    let localPath = process.cwd();
    let remotePath = "/";

    async function listLocal() {
        try {
            const files = await fs.promises.readdir(localPath);
            return files.sort();
        } catch {
            return [];
        }
    }

    async function listRemote() {
        try {
            const list = await client.list();
            return list.map(entry => entry.name).sort();
        } catch {
            return [];
        }
    }

    async function download(file) {
        try {
            await client.downloadTo(path.join(localPath, file), file);
            console.log("Скачано:", file);
        } catch (err) {
            console.log("Ошибка скачивания:", err.message);
        }
    }

    async function upload(file) {
        try {
            await client.uploadFrom(path.join(localPath, file), file);
            console.log("Загружено:", file);
        } catch (err) {
            console.log("Ошибка загрузки:", err.message);
        }
    }

    rl.on('line', async (input) => {
        const cmd = input.trim();
        if (cmd === 'q' || cmd === 'exit') {
            client.close();
            rl.close();
            return;
        }
        if (cmd.startsWith('cd ')) {
            const dir = cmd.slice(3);
            const newPath = path.join(localPath, dir);
            try {
                const stat = await fs.promises.stat(newPath);
                if (stat.isDirectory()) {
                    localPath = newPath;
                }
            } catch {}
        } else if (cmd.startsWith('cdr ')) {
            const dir = cmd.slice(4);
            try {
                await client.cd(dir);
                remotePath = await client.pwd();
            } catch {}
        } else if (cmd.startsWith('get ')) {
            const file = cmd.slice(4);
            await download(file);
        } else if (cmd.startsWith('put ')) {
            const file = cmd.slice(4);
            await upload(file);
        } else {
            console.log('Неизвестная команда');
        }
        display();
    });

    async function display() {
        const local = await listLocal();
        const remote = await listRemote();
        console.clear();
        console.log('FTPCommander (JS) - test.rebex.net');
        console.log('Локальная:', localPath);
        console.log('Удалённая:', remotePath);
        console.log('--- Локальная ---');
        local.slice(0, 10).forEach(f => console.log(f));
        console.log('--- Удалённая ---');
        remote.slice(0, 10).forEach(f => console.log(f));
        console.log('Команды: cd, cdr, get, put, q');
        console.log('> ');
    }

    display();
}

main().catch(console.error);
