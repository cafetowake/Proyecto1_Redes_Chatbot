# Capturing remote MCP traffic

Steps to capture and decrypt the HTTPS traffic between the chatbot and
the remote MCP server deployed on Render.

## 1. Wake up the service before capturing

Render puts the service to sleep after 15 minutes without traffic.
Send a request to wake it up first, so the cold start delay doesn't
get mixed into the capture:

    curl -X POST https://proyecto1-redes-chatbot.onrender.com -d '{"jsonrpc":"2.0","id":0,"method":"tools/list"}'

## 2. Set the environment variable for the TLS session keys

    $env:SSLKEYLOGFILE = "$PWD\tls_keys.log"
    $env:PHARMACY_REMOTE_URL = "https://proyecto1-redes-chatbot.onrender.com"

## 3. Configure Wireshark to decrypt TLS

Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log filename,
point it to the same tls_keys.log file.

## 4. Start the capture

Active network interface, with capture filter:

    tcp port 443

## 5. Generate the traffic

    python capture_session.py

## 6. Stop the capture and save

Save as pharmacy_remote_capture.pcapng in this same folder.