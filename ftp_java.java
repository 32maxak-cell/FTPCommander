// ftp_java.java — двухпанельный FTP-клиент на Java (Apache Commons Net)

import org.apache.commons.net.ftp.FTPClient;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.net.SocketException;

public class FTPCommander {
    private static FTPClient ftp;
    private static String localPath = System.getProperty("user.dir");
    private static String remotePath = "/";
    private static List<String> localFiles = new ArrayList<>();
    private static List<String> remoteFiles = new ArrayList<>();

    public static void main(String[] args) {
        try {
            ftp = new FTPClient();
            ftp.connect("test.rebex.net");
            ftp.login("demo", "password");
            ftp.enterLocalPassiveMode();
        } catch (Exception e) {
            System.out.println("Ошибка подключения: " + e.getMessage());
            return;
        }

        Scanner sc = new Scanner(System.in);
        while (true) {
            listLocal();
            listRemote();
            printPanel();
            System.out.print("> ");
            String cmd = sc.nextLine().trim();
            if (cmd.equals("q") || cmd.equals("exit")) break;
            else if (cmd.startsWith("cd ")) {
                String dir = cmd.substring(3);
                try {
                    Paths.get(localPath, dir).toFile().isDirectory();
                    localPath = Paths.get(localPath, dir).toString();
                } catch (Exception e) {}
            } else if (cmd.startsWith("cdr ")) {
                String dir = cmd.substring(4);
                try {
                    if (ftp.changeWorkingDirectory(dir)) {
                        remotePath = ftp.printWorkingDirectory();
                    }
                } catch (IOException e) {}
            } else if (cmd.startsWith("get ")) {
                String file = cmd.substring(4);
                download(file);
            } else if (cmd.startsWith("put ")) {
                String file = cmd.substring(4);
                upload(file);
            }
        }
        try { ftp.disconnect(); } catch (IOException e) {}
        sc.close();
    }

    static void listLocal() {
        localFiles.clear();
        File dir = new File(localPath);
        if (dir.isDirectory()) {
            for (File f : dir.listFiles()) {
                if (f.isDirectory()) localFiles.add(f.getName() + "/");
                else localFiles.add(f.getName());
            }
        }
        Collections.sort(localFiles);
    }

    static void listRemote() {
        remoteFiles.clear();
        try {
            for (String name : ftp.listNames()) {
                remoteFiles.add(name);
            }
        } catch (IOException e) {}
        Collections.sort(remoteFiles);
    }

    static void printPanel() {
        System.out.println("FTPCommander (Java) - test.rebex.net");
        System.out.println("Локальная: " + localPath);
        System.out.println("Удалённая: " + remotePath);
        System.out.println("--- Локальная ---");
        for (int i=0; i<Math.min(10, localFiles.size()); i++) {
            System.out.println((i+1) + ". " + localFiles.get(i));
        }
        System.out.println("--- Удалённая ---");
        for (int i=0; i<Math.min(10, remoteFiles.size()); i++) {
            System.out.println((i+1) + ". " + remoteFiles.get(i));
        }
        System.out.println("Команды: cd, cdr, get, put, q");
    }

    static void download(String file) {
        try (FileOutputStream fos = new FileOutputStream(Paths.get(localPath, file).toString())) {
            ftp.retrieveFile(file, fos);
            System.out.println("Скачано: " + file);
        } catch (IOException e) {
            System.out.println("Ошибка скачивания");
        }
    }

    static void upload(String file) {
        try (FileInputStream fis = new FileInputStream(Paths.get(localPath, file).toString())) {
            ftp.storeFile(file, fis);
            System.out.println("Загружено: " + file);
        } catch (IOException e) {
            System.out.println("Ошибка загрузки");
        }
    }
}
