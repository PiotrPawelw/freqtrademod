import slixmpp
import json

class XMPPClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password, rpc_handler):
        super().__init__(jid, password)
        self.rpc_handler = rpc_handler
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        # Konfiguracja połączenia bez SSL/TLS
        self.use_tls = True
        self.use_ssl = True
        self.default_port=5222

    async def start(self, event):
        print("Connected to XMPP server.")
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            try:
                # Obsługa wiadomości i wywoływanie RPC
                data = json.loads(msg['body'])
                command = data.get('command')
                params = data.get('params', {})
                result = self.rpc_handler(command, params)
                response = json.dumps({"status": "success", "result": result})
            except Exception as e:
                response = json.dumps({"status": "error", "message": str(e)})
            msg.reply(response).send()

# Definicja funkcji `rpc_handler`
def rpc_handler(command, params):
    # Obsługa prostych komend RPC
    if command == "start_process":
        process_id = params.get("process_id", "unknown")
        return f"Process {process_id} started."
    elif command == "stop_process":
        process_id = params.get("process_id", "unknown")
        return f"Process {process_id} stopped."
    else:
        return "Unknown command"

# Konfiguracja klienta
jid = "trader@niemazartow.eu"
password = "a"

# Tworzenie instancji klienta
xmpp = XMPPClient(jid, password, rpc_handler)
xmpp.connect()
xmpp.process()
