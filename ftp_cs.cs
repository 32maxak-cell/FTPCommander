// ftp_cs.cs — двухпанельный FTP-клиент на C# (FluentFTP)

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using FluentFTP;

class FTPCommander
{
    static FtpClient ftp;
    static string localPath = Directory.GetCurrentDirectory();
    static string remotePath = "/";
    static List<string> localFiles = new List<string>();
    static List<string> remoteFiles = new List<string>();

    public static void Main()
    {
        ftp = new FtpClient("test.rebex.net", "demo", "password");
        ftp.Connect();
        while (true)
        {
            listLocal();
            listRemote();
            printPanel();
            Console.Write("> ");
            string cmd = Console.ReadLine().Trim();
            if (cmd == "q" || cmd == "exit") break;
            else if (cmd.StartsWith("cd "))
            {
                string dir = cmd.Substring(3);
                string newPath = Path.Combine(localPath, dir);
                if (Directory.Exists(newPath))
                {
                    localPath = newPath;
                }
            }
            else if (cmd.StartsWith("cdr "))
            {
                string dir = cmd.Substring(4);
                if (ftp.SetWorkingDirectory(dir))
                {
                    remotePath = ftp.GetWorkingDirectory();
                }
            }
            else if (cmd.StartsWith("get "))
            {
                string file = cmd.Substring(4);
                ftp.DownloadFile(Path.Combine(localPath, file), file);
                Console.WriteLine("Скачано");
            }
            else if (cmd.StartsWith("put "))
            {
                string file = cmd.Substring(4);
                ftp.UploadFile(Path.Combine(localPath, file), file);
                Console.WriteLine("Загружено");
            }
        }
        ftp.Disconnect();
    }

    static void listLocal()
    {
        localFiles = Directory.GetFileSystemEntries(localPath).Select(Path.GetFileName).ToList();
        localFiles.Sort();
    }

    static void listRemote()
    {
        remoteFiles = ftp.GetNameListing().ToList();
        remoteFiles.Sort();
    }

    static void printPanel()
    {
        Console.Clear();
        Console.WriteLine("FTPCommander (C#) - test.rebex.net");
        Console.WriteLine("Локальная: " + localPath);
        Console.WriteLine("Удалённая: " + remotePath);
        Console.WriteLine("--- Локальная ---");
        foreach (var f in localFiles.Take(10))
            Console.WriteLine(f);
        Console.WriteLine("--- Удалённая ---");
        foreach (var f in remoteFiles.Take(10))
            Console.WriteLine(f);
        Console.WriteLine("Команды: cd, cdr, get, put, q");
    }
}
