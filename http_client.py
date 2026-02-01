"""
HTTP Client for CPAN-226 Assignment
Student Name: Harry Joseph
Student ID: N00881767
Date: January 30, 2026
"""

from socket import *
import ssl

# Server configuration
server_name = 'gaia.cs.umass.edu'

# Choose HTTP or HTTPS
print("Choose protocol:")
print("1) HTTP (port 80) — expected 301 redirect")
print("2) HTTPS (port 443) — expected 200 OK")
choice = input("Enter 1 or 2: ").strip()

use_https = choice == "2"
server_port = 443 if use_https else 80

# Step 1: Create a TCP socket (IPv4)
# AF_INET = IPv4 addressing; SOCK_STREAM = TCP socket type.
base_socket = socket(AF_INET, SOCK_STREAM)
client_socket = base_socket

try:
    # Step 2: Connect to the server.
    client_socket.connect((server_name, server_port))
    if use_https:
        context = ssl.create_default_context()
        client_socket = context.wrap_socket(client_socket, server_hostname=server_name)
    print(f"Connected to {server_name}:{server_port}")

    # Step 3: Prepare the HTTP request.
    # HTTP requires \r\n (CRLF) line endings.
    # Double \r\n indicates the end of headers.
    request = (
        "GET /kurose_ross/interactive/index.php HTTP/1.1\r\n"
        "Host: gaia.cs.umass.edu\r\n"
        "\r\n"
    )

    # Step 4: Send the request (encode string to bytes).
    client_socket.send(request.encode())
    print("Request sent successfully")

    # Step 5: Receive the response (up to 4096 bytes).
    response = client_socket.recv(4096)

    # Step 6: Decode and print the result.
    decoded_response = response.decode(errors='replace')
    print("\n" + "=" * 50)
    print("SERVER RESPONSE:")
    print("=" * 50)
    print(decoded_response)

    # Extract the status line for analysis.
    if decoded_response.startswith("HTTP/"):
        status_line = decoded_response.split('\r\n')[0]
        print(f"\nStatus Line: {status_line}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Step 7: Close the connection.
    client_socket.close()
    print("\nConnection closed")
