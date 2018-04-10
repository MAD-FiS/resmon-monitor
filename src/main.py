import sys
sys.path.append('./Server/src')
import Server
import threading
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sensor monitor', \
        epilog='Example usage: python3 main.py -p 8083 -c ./cert.pem -k ./key.pm')
    parser.add_argument('-p', '--port', required=True, type=int, help='Server port')
    parser.add_argument('-c', '--cert', required=True, help='Cert path')
    parser.add_argument('-k', '--key', required=True, help='Certificate key path')
    args = parser.parse_args()

    server = Server.Server('localhost', args.port, args.key, args.cert)
    while True:
        if not server.is_running:
            threading.Thread(target=server.listen).start()
