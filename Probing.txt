on the phone, settings/developer options, click the Bug Report button.  The interactive mode shares it by email/etc.; full report is picked up by

`adb bugreport anewbugreportfolder`

then Wireshark to FS/data/log/bt/btsnoop_hci.log

In Wireshark - look for write commands, sent by the phone - view payloads, note seems to default to EBCDIC instead of ASCII.  Note the attribute values it was sent to - and use these in the code.


Try manually to connect:
```
bluetoothcl
scan on
power on
pairable on
discoverable on
connect
gatt.list-attributes
```

