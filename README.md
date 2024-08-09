A simple reader for Gran Turismo 7's telemetry transmitted by the game via UDP

Parts of this application refer to previous work by others:
-   Salsa20 decryption of the packet: https://github.com/lmirel/mfc/blob/master/clients/gt7racedata.py
-   Breakdown of the packet data: https://github.com/snipem/go-gt7-telemetry/blob/main/lib/gt7data.go

>[!NOTE]
>Set the local IP address of your PlayStation in config/udp.py PS5_IP

>[!WARNING]
>The pre-built release (releases/GTMonitor.zip) will not work until a way of providing an IP address via the GUI is implemented.

https://github.com/user-attachments/assets/36388ea2-d4f2-4b8a-b924-c3fcf9c9591b
