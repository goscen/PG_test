from argparse import ArgumentParser
import time
from getpass import getpass
from socket import gethostbyname
import paramiko


def install(hostname: str, use_pass: str, username: str, port: int):
    with paramiko.SSHClient() as cli:
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if use_pass == "yes":
            password = getpass("Enter password for host")
            cli.connect(hostname=hostname, username=username,
                        password=password, allow_agent=False, look_for_keys=False, port=port)
        else:
            cli.connect(hostname=hostname, username=username, allow_agent=True, look_for_keys=True, port=port)
        ssh = cli.invoke_shell()
        ssh.send("env\n")
        time.sleep(1)
        print(ssh.recv(1000))


if __name__ == '__main__':
    parser = ArgumentParser(description="Install postgresql DB on remote host")
    parser.add_argument("destination", type=str, help="Enter host(ip/hostname)")
    parser.add_argument("-p", type=str, default="no", required=False, choices=["yes", "no"],
                        help="Use password to connect remote host")
    parser.add_argument("-P", type=int, default=22, required=False, help="Enter ssh port")
    parser.add_argument("-u", type=str, required=True, help="Enter username")
    args = parser.parse_args()
    try:
        ip = gethostbyname(args.destination)
    except Exception as err:
        raise Exception("wrong host or ip")
    install(args.destination, args.p, args.u, abs(args.P))
