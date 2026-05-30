# Coding utf-8
import socket
import json
import threading
import queue
import base64
import random
import time

class NetworkManager:
    def __init__(self):
        self.socket = None
        self.conn = None
        self.rx_queue = queue.Queue()
        self.is_host = False
        self.connected = False
        self.host_ip = ""
        self.port = 5555
        self.thread = None
        self.running = False

    def get_local_ip(self):
        # Récupère l'adresse IP locale de la machine sur le réseau local
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Utilise une IP externe factice pour forcer le système à choisir l'interface active
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start_host(self):
        self.is_host = True
        self.host_ip = self.get_local_ip()
        self.running = True
        self.connected = False
        self.conn = None
        # Vider la file d'attente
        while not self.rx_queue.empty():
            try:
                self.rx_queue.get_nowait()
            except queue.Empty:
                break
        self.thread = threading.Thread(target=self._host_loop, daemon=True)
        self.thread.start()

    def _host_loop(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind(("", self.port))
            server_socket.listen(1)
            server_socket.settimeout(1.0)  # timeout pour pouvoir quitter la boucle proprement
            print(f"Server listening on port {self.port}...")
            while self.running and not self.connected:
                try:
                    conn, addr = server_socket.accept()
                    self.conn = conn
                    self.connected = True
                    print(f"Connected to client: {addr}")
                    self.rx_queue.put({"type": "connected", "addr": addr[0]})
                    # Lancer le thread de réception
                    threading.Thread(target=self._recv_loop, daemon=True).start()
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"Server error: {e}")
            self.rx_queue.put({"type": "connection_failed", "error": str(e)})
        finally:
            server_socket.close()

    def start_client(self, ip):
        self.is_host = False
        self.host_ip = ip
        self.running = True
        self.connected = False
        self.conn = None
        # Vider la file d'attente
        while not self.rx_queue.empty():
            try:
                self.rx_queue.get_nowait()
            except queue.Empty:
                break
        self.thread = threading.Thread(target=self._client_connect_loop, daemon=True)
        self.thread.start()

    def _client_connect_loop(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5.0)  # 5 secondes de timeout pour la connexion
        try:
            print(f"Attempting to connect to host {self.host_ip}:{self.port}...")
            client_socket.connect((self.host_ip, self.port))
            self.conn = client_socket
            self.connected = True
            print("Connected to host successfully!")
            self.rx_queue.put({"type": "connected", "addr": self.host_ip})
            # Lancer le thread de réception
            threading.Thread(target=self._recv_loop, daemon=True).start()
        except Exception as e:
            print(f"Client connection error: {e}")
            self.rx_queue.put({"type": "connection_failed", "error": str(e)})

    def _recv_loop(self):
        self.conn.setblocking(True)
        buffer = ""
        while self.running:
            try:
                data = self.conn.recv(4096).decode('utf-8')
                if not data:
                    # Connexion fermée proprement par l'autre bout
                    self.rx_queue.put({"type": "disconnected"})
                    self.connected = False
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        msg = json.loads(line)
                        self.rx_queue.put(msg)
            except Exception as e:
                print(f"Receive error: {e}")
                self.rx_queue.put({"type": "disconnected"})
                self.connected = False
                break

    def send(self, msg):
        if self.conn:
            try:
                data = json.dumps(msg) + "\n"
                self.conn.sendall(data.encode('utf-8'))
                return True
            except Exception as e:
                print(f"Send error: {e}")
                return False
        return False

    def get_message(self):
        # Renvoie un message de la queue si disponible, sinon None
        try:
            return self.rx_queue.get_nowait()
        except queue.Empty:
            return None

    def disconnect(self):
        self.running = False
        self.connected = False
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
        print("Disconnected network manager.")


class InternetNetworkManager:
    def __init__(self):
        self.connected = False
        self.is_host = False
        self.rx_queue = queue.Queue()
        self.running = False
        
        self.opponent_nick = ""
        self.my_nick = ""
        self.my_id = random.randint(100000, 999999)
        self.lobby_channel = "#fairy_card_matchmaking_lobby"
        self.irc_server = "irc.oftc.net"
        self.irc_port = 6667
        
        self.sock = None
        self.thread = None

    def start_matchmaking(self):
        self.running = True
        self.connected = False
        self.is_host = False
        # Clear rx queue
        while not self.rx_queue.empty():
            try:
                self.rx_queue.get_nowait()
            except queue.Empty:
                break
                
        self.thread = threading.Thread(target=self._matchmaking_loop, daemon=True)
        self.thread.start()

    def _matchmaking_loop(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10.0)
            print(f"Connecting to matchmaking server {self.irc_server}:{self.irc_port}...")
            self.sock.connect((self.irc_server, self.irc_port))
            self.sock.settimeout(1.5)
            
            # Generate random nickname (Keep under 15 characters for QuakeNet)
            self.my_nick = f"Fairy_{random.randint(100000, 999999)}"
            
            # Register user
            self.sock.send(f"USER {self.my_nick} 0 * :Fairy Card Player\r\n".encode("utf-8"))
            self.sock.send(f"NICK {self.my_nick}\r\n".encode("utf-8"))
            
            buffer = ""
            connected_irc = False
            last_search_send = 0
            
            # Step 1: Wait for Welcome message and JOIN lobby
            while self.running and not self.connected:
                try:
                    data = self.sock.recv(4096).decode("utf-8", errors="ignore")
                    if not data:
                        print("Matchmaking connection lost.")
                        self.rx_queue.put({"type": "connection_failed", "error": "Connection lost"})
                        break
                    buffer += data
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        
                        # Respond to PING
                        if line.startswith("PING"):
                            ping_challenge = line.split()[1]
                            self.sock.send(f"PONG {ping_challenge}\r\n".encode("utf-8"))
                            
                        # Connected to IRC!
                        if " 001 " in line or " 376 " in line or "Welcome" in line:
                            if " 001 " in line:
                                try:
                                    parts = line.split(" 001 ")
                                    self.my_nick = parts[1].split()[0]
                                    print(f"Matchmaking nickname confirmed: {self.my_nick}")
                                except Exception:
                                    pass
                            if not connected_irc:
                                connected_irc = True
                                print("Connected to IRC lobby server!")
                                self.sock.send(f"JOIN {self.lobby_channel}\r\n".encode("utf-8"))
                                
                        # Parse channel messages and direct messages
                        if connected_irc:
                            self._parse_irc_line(line)
                            
                except socket.timeout:
                    # Timeout is normal, let's keep running and check matchmaking/searching
                    pass
                except Exception as e:
                    print(f"IRC matchmaking error during read: {e}")
                    self.rx_queue.put({"type": "connection_failed", "error": str(e)})
                    break
                
                # Periodically send matchmaking broadcast if in lobby
                if connected_irc and self.running and not self.connected:
                    now = time.time()
                    if now - last_search_send >= 2.5:
                        try:
                            self.sock.send(f"PRIVMSG {self.lobby_channel} :FC_SEARCH_{self.my_id}\r\n".encode("utf-8"))
                            last_search_send = now
                        except Exception as e:
                            print(f"Failed to send matchmaking ping: {e}")
                            break
                            
            # Step 2: Once connected, enter active game relay loop
            if self.connected:
                self._game_relay_loop(buffer)
                
        except Exception as e:
            print(f"IRC connection failed: {e}")
            self.rx_queue.put({"type": "connection_failed", "error": str(e)})
        finally:
            self.disconnect()

    def _parse_irc_line(self, line):
        # Format of channel or PM: :Sender!User@Host PRIVMSG Target :Message
        if "PRIVMSG" in line:
            parts = line.split("PRIVMSG", 1)
            sender_prefix = parts[0].strip()
            msg_part = parts[1].strip()
            
            # Extract sender nick
            sender_nick = ""
            if sender_prefix.startswith(":"):
                sender_nick = sender_prefix[1:].split("!", 1)[0]
                
            # Extract target and message content
            if " :" in msg_part:
                target, content = msg_part.split(" :", 1)
                target = target.strip()
                content = content.strip()
                
                # Check matchmaking broadcasts in lobby channel
                if target.lower() == self.lobby_channel.lower():
                    if content.startswith("FC_SEARCH_"):
                        try:
                            other_id = int(content.split("FC_SEARCH_")[1])
                            # If another client is searching and we haven't matched yet
                            if other_id != self.my_id and not self.connected:
                                # Proposer is the one with the larger ID to avoid collision
                                if self.my_id > other_id:
                                    print(f"Found opponent {sender_nick} ({other_id})! Proposing match...")
                                    self.sock.send(f"PRIVMSG {sender_nick} :FC_PROPOSE_{self.my_id}_{other_id}\r\n".encode("utf-8"))
                        except ValueError:
                            pass
                            
                # Check direct private messages to us
                elif target.lower() == self.my_nick.lower():
                    if content.startswith("FC_PROPOSE_"):
                        try:
                            # Format: FC_PROPOSE_<proposer_id>_<target_id>
                            parts = content.split("_")
                            proposer_id = int(parts[2])
                            target_id = int(parts[3])
                            
                            if target_id == self.my_id and not self.connected:
                                print(f"Received match proposal from {sender_nick} ({proposer_id}). Accepting...")
                                self.sock.send(f"PRIVMSG {sender_nick} :FC_ACCEPT_{self.my_id}_{proposer_id}\r\n".encode("utf-8"))
                                
                                # Set state: smaller ID is host
                                self.opponent_nick = sender_nick
                                self.is_host = True  # We are the target of proposal, so our ID < proposer_id. We are host!
                                self.connected = True
                                self.rx_queue.put({"type": "connected", "addr": self.opponent_nick})
                        except (ValueError, IndexError):
                            pass
                            
                    elif content.startswith("FC_ACCEPT_"):
                        try:
                            # Format: FC_ACCEPT_<accepter_id>_<proposer_id>
                            parts = content.split("_")
                            accepter_id = int(parts[2])
                            proposer_id = int(parts[3])
                            
                            if proposer_id == self.my_id and not self.connected:
                                print(f"Match proposal accepted by {sender_nick} ({accepter_id})!")
                                
                                # Set state: smaller ID is host
                                self.opponent_nick = sender_nick
                                self.is_host = False  # We are the proposer, so our ID > accepter_id. We are client!
                                self.connected = True
                                self.rx_queue.put({"type": "connected", "addr": self.opponent_nick})
                        except (ValueError, IndexError):
                            pass

    def _game_relay_loop(self, initial_buffer):
        self.sock.setblocking(True)
        buffer = initial_buffer
        while self.running and self.connected:
            try:
                data = self.sock.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    print("Game connection to IRC server lost.")
                    self.rx_queue.put({"type": "disconnected"})
                    self.connected = False
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    
                    # Keepalive
                    if line.startswith("PING"):
                        ping_challenge = line.split()[1]
                        self.sock.send(f"PONG {ping_challenge}\r\n".encode("utf-8"))
                        continue
                        
                    # Parse private messages containing game data
                    if "PRIVMSG" in line:
                        parts = line.split("PRIVMSG", 1)
                        sender_prefix = parts[0].strip()
                        msg_part = parts[1].strip()
                        
                        sender_nick = ""
                        if sender_prefix.startswith(":"):
                            sender_nick = sender_prefix[1:].split("!", 1)[0]
                            
                        if sender_nick.lower() == self.opponent_nick.lower() and " :" in msg_part:
                            target, content = msg_part.split(" :", 1)
                            target = target.strip()
                            content = content.strip()
                            
                            if target.lower() == self.my_nick.lower():
                                if content.startswith("FC_DATA_"):
                                    encoded = content.split("FC_DATA_")[1]
                                    try:
                                        data_str = base64.b64decode(encoded.encode("utf-8")).decode("utf-8")
                                        msg = json.loads(data_str)
                                        self.rx_queue.put(msg)
                                    except Exception as e:
                                        print(f"Failed to decode game message: {e}")
                                elif content == "FC_QUIT":
                                    print("Opponent quit the game.")
                                    self.rx_queue.put({"type": "disconnected"})
                                    self.connected = False
                                    break
            except Exception as e:
                print(f"Game receive error: {e}")
                self.rx_queue.put({"type": "disconnected"})
                self.connected = False
                break

    def send(self, msg):
        if self.sock and self.connected:
            try:
                data_str = json.dumps(msg)
                encoded = base64.b64encode(data_str.encode("utf-8")).decode("utf-8")
                self.sock.send(f"PRIVMSG {self.opponent_nick} :FC_DATA_{encoded}\r\n".encode("utf-8"))
                return True
            except Exception as e:
                print(f"Send error over IRC: {e}")
                return False
        return False

    def get_message(self):
        try:
            return self.rx_queue.get_nowait()
        except queue.Empty:
            return None

    def disconnect(self):
        self.running = False
        self.connected = False
        if self.sock:
            try:
                if self.opponent_nick:
                    # Notify opponent we are leaving
                    self.sock.send(f"PRIVMSG {self.opponent_nick} :FC_QUIT\r\n".encode("utf-8"))
                self.sock.send(b"QUIT :Leaving Game\r\n")
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        print("Disconnected internet network manager.")
