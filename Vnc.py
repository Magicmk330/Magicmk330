import pyautogui
import socket
import struct
import sys

# Define VNC server settings
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
VNC_PORT = 5900

# Function to send VNC protocol message
def send_vnc_message(sock, message):
    sock.sendall(struct.pack('!B', message))

# Function to handle client connections
def handle_client(conn):
    # Send VNC protocol version message
    send_vnc_message(conn, 3)

    # Send VNC security type message
    send_vnc_message(conn, 1)

    # Send VNC security result message
    send_vnc_message(conn, 0)

    # Send VNC desktop size message
    send_vnc_message(conn, 0)
    send_vnc_message(conn, 0)
    send_vnc_message(conn, 0)
    send_vnc_message(conn, SCREEN_WIDTH)
    send_vnc_message(conn, 0)
    send_vnc_message(conn, SCREEN_HEIGHT)

    try:
        while True:
            # Capture screen image
            image = pyautogui.screenshot()

            # Send VNC framebuffer update message
            send_vnc_message(conn, 0)
            send_vnc_message(conn, 0)
            send_vnc_message(conn, 0)
            send_vnc_message(conn, SCREEN_WIDTH)
            send_vnc_message(conn, 0)
            send_vnc_message(conn, SCREEN_HEIGHT)
            send_vnc_message(conn, 8)
            send_vnc_message(conn, 0)

            # Send screen image data
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    color = image.getpixel((x, y))
                    r, g, b = color[0], color[1], color[2]
                    send_vnc_message(conn, (r << 16) | (g << 8) | b)

    except Exception as e:
        print(f"Error: {e}")
        conn.close()

# Main program
def main():
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to localhost and VNC port
    server_socket.bind(('localhost', VNC_PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Listening on port {VNC_PORT}")

    try:
        while True:
            # Accept client connection
            conn, addr = server_socket.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            # Handle client connection
            handle_client(conn)

    except KeyboardInterrupt:
        print("Server stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
