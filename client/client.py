#!/usr/bin/python
import traceback
import re
import requests
from requests.exceptions import HTTPError, ChunkedEncodingError, ConnectionError
import argparse


import asyncio
import sys
import platform
from bleak import BleakClient, BleakScanner, BleakCharacteristicNotFoundError

# Define the UUIDs based on your service/characteristic shorthand
# Note: Full 128-bit UUIDs are often required if these are custom
#SERVICE_UUID = 


async def g_e7(client):
    try:
        payload = "TCWAKEUP".encode('utf-8')
        CHAR_UUID    = "0000ffb1-0000-1000-8000-00805f9b34fb"
        
        print(f"Sending payload to {CHAR_UUID}...")
        # write_gatt_char sends data to the device
        await client.write_gatt_char(CHAR_UUID, payload)
        print("Payload sent successfully.")
    except BleakCharacteristicNotFoundError as e:
        await g_e8(client)
        
async def g_e8(client):
    payload = "AT+WAKEPULSE=10\r\n".encode('utf-8')
    CHAR_UUID    = "6e400004-b5a3-f393-e0a9-e50e24dcca9e"
    print(f"Sending payload to {CHAR_UUID}...")
    # write_gatt_char sends data to the device
    await client.write_gatt_char(CHAR_UUID, payload)
    
    print("Payload sent successfully.")

async def scan(bt_local_id):
    print("Scanning bluetooth")
    devices = await BleakScanner.discover(bluez = {"adapter" : bt_local_id}, timeout = 30)
    print(f"\nFound {len(devices)} devices:")
    print("-" * 40)
    
    for device in devices:
        # Some devices don't broadcast a name, so we provide a default
        name = device.name if device.name else "Unknown/No Name"
        print(f"Address: {device.address} | Name: {name}")
    return devices;


async def run(bt_local_id, address, wifi_id, password):
    devices = await scan(bt_local_id)
    print(f"Searching for and connecting to {address}...")

    devices = filter(lambda x : (x.name and x.name.startswith(address)) or x.address.startswith(address), devices)
    for device in devices:
        try:
            fresh_handle = await BleakScanner.find_device_by_filter(
                lambda x, n : x.address.lower() == device.address.lower(), timeout=20.0)

            if not fresh_handle:
                print(f"Could not find device {device.address.lower()}" )
                continue
            async with BleakClient(fresh_handle, bluez = {"adapter" : bt_local_id}, timeout=30.0) as client:
                if client.is_connected:
                    if is_macos():
                        check = run_command("system_profiler SPBluetoothDataType")
                        print(f"{check.stdout.strip()}")
                        r = re.compile(fr'{device.name}:\s+Address: (.+)$', re.MULTILINE)
                        m = r.search(check.stdout)
                        if m is None:
                            print("Unable to read BT address - cannot find WiFi without it on OS/X")
                            return
                        addr = m.group(1)
                    else:
                        addr = client.address
                                 
                    print(f"Connected to {address}")
                    name = client.name
                    print(f"name is {client.name}")
                    # Convert text payload to bytes

                    if name.endswith("G_E8"):
                        await g_e8(client)
                    else:
                        await g_e7(client)
                else:
                    print(f"Failed to connect to {address}")

                if connect_to_cam_wifi(wifi_id, addr, password):
                    session = requests.Session()
                    adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
                    session.mount('http://', adapter)
                    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=requests.adapters.Retry(total=5, backoff_factor=.1))) # add this as chunked responses are quite unreliable with the device
                    while process_images(session) > 0:
                        pass

        except Exception as e:
            print(f"An error occurred: {e}")
            print(traceback.print_exc())
        

import subprocess
import time
import sys

def run_command(command):
    """Helper to run shell commands and return output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

def is_macos():
    """Check if the operating system is macOS."""
    return platform.system() == "Darwin"

def connect_to_cam_wifi_linux(device, cam_mac, password=None):
    """Connect to camera WiFi on Linux using nmcli."""
    device_string = f" ifname {device}" if device else ""

    print("Pause to enable Wi-Fi network activation...")
    time.sleep(10) 
    print("Scanning for Wi-Fi networks...")
    retry = 0
    while retry < 4:
        
    # Rescan to ensure the list is fresh
        run_command(f"nmcli device wifi rescan {device_string}")
        time.sleep(15) # Give the radio a moment to populate results

        # List available Wi-Fi SSIDs
        cmd = f"nmcli -t -f SSID device wifi list {device_string}"
        scan_result = run_command(cmd)
        if scan_result.returncode != 0:
            print(cmd)
            print(scan_result)
            print("Error: Could not scan for Wi-Fi. Is your Wi-Fi turned on?")
            return False

        # Split output into a list of SSIDs and filter for those starting with 'CAM'
        ssids = scan_result.stdout.strip().split('\n')
        target_ssid = next((s for s in ssids if s.startswith("CAM")), None)
        
        if not target_ssid:
            print(f"No Wi-Fi network starting with 'CAM' was found (retry {retry}).")
            print(scan_result.stdout)
        else:
            break
        retry += 1

    if not target_ssid:
        return False
    print(f"Found network: {target_ssid}. Attempting to connect...")

    # Construct the connection command
    if password:
        cmd = f"nmcli device wifi connect '{target_ssid}' password '{password}' {device_string}"
    else:
        cmd = f"nmcli device wifi connect '{target_ssid}' {device_string}"

    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully connected to {target_ssid}!")
        return True
    else:
        print(f"Failed to connect: {connect_result.stderr.strip()}")
        return False

def connect_to_cam_wifi_macos_networksetup(device, cam_mac, password=None):
    """Fallback: Connect to camera WiFi on macOS using only networksetup (no airport scanning)."""
    print("Using networksetup-only method to connect to camera WiFi...")
    
    # First, make sure WiFi is turned on
    print("Turning on WiFi...")
    wifi_power = run_command("sudo networksetup -setairportpower en0 on")
    if wifi_power.returncode != 0:
        print(f"Warning: Could not turn on WiFi: {wifi_power.stderr}")
    time.sleep(5)
    
    # Assuming the camera WiFi network name is known or we try common patterns
    # Try to find CAM networks by attempting connection
    retry = 0
    while retry < 4:
        print(f"Attempting to connect to camera WiFi network (attempt {retry + 1}/4)...")

        # Try common camera WiFi patterns
        for cam_pattern in [f'CAM8Z8_{cam_mac.replace(":","")}']:
            
            if password:
                cmd = f"sudo networksetup -setairportnetwork en0 '{cam_pattern}' '{password}'"
                print(cmd)
            else:
                cmd = f"sudo networksetup -setairportnetwork en0 '{cam_pattern}'"
            
            connect_result = run_command(cmd)
            
            if connect_result.returncode == 0:
                print(f"Successfully connected to {cam_pattern}!")
                time.sleep(5)
                
                # Check current WiFi connection
                wifi_check = run_command("networksetup -getairportnetwork en0")
                print(f"Current WiFi: {wifi_check.stdout.strip()}")
                
                # Check IP address
                ip_check = run_command("ifconfig en0 | grep 'inet ' | awk '{print $2}'")
                print(f"IP Address: {ip_check.stdout.strip()}")
                
                # If still no IP, wait longer and try again
                if not ip_check.stdout.strip():
                    print("No IP assigned yet, waiting longer...")
                    time.sleep(10)
                    ip_check = run_command("ifconfig en0 | grep 'inet ' | awk '{print $2}'")
                    print(f"IP Address after wait: {ip_check.stdout.strip()}")
                
                # Try to ping the camera
                ping_result = run_command("ping -c 3 -W 2 192.168.8.1")
                if ping_result.returncode == 0:
                    print("Camera is reachable!")
                    print(f"Connection successful!")
                else:
                    print("Warning: Camera not reachable yet, waiting longer...")
                    time.sleep(10)
                    # Try ping again
                    ping_result = run_command("ping -c 3 -W 2 192.168.8.1")
                    if ping_result.returncode == 0:
                        print("Camera is now reachable!")
                    else:
                        print("Still cannot reach camera")
                print(f"WiFi should now be ready")
                return True
            else:
                print(f"Connection attempt to {cam_pattern} failed: {connect_result.stderr}")
                print(f"Return code: {connect_result.returncode}")
            
        retry += 1
    
    print("Failed to connect using networksetup method")
    return False

def connect_to_cam_wifi_macos(device, cam_mac, password=None):
    """Connect to camera WiFi on macOS using networksetup."""
    
    # First, make sure WiFi is turned on
    print("Turning on WiFi...")
    wifi_power = run_command("sudo networksetup -setairportpower en0 on")
    if wifi_power.returncode != 0:
        print(f"Warning: Could not turn on WiFi: {wifi_power.stderr}")
    time.sleep(5)
    
    return connect_to_cam_wifi_macos_networksetup(device, cam_mac, password)
    

def connect_to_cam_wifi(device, cam_mac, password=None):
    """Platform-agnostic function to connect to camera WiFi."""
    if is_macos():
        return connect_to_cam_wifi_macos(device, cam_mac, password)
    else:
        return connect_to_cam_wifi_linux(device, cam_mac, password)

        
base_url = "http://192.168.8.1:8080"


def cam_reset(session):
    reset_url = base_url + "/cmd/standby/reset"
    response = session.get(reset_url)
    data = response.json()
    
def get_cam_id(session):
    info_url = base_url + "/cmd/getSetting"
    response = session.get(info_url)
    data = response.json()
    print(data)
    return data["data"]["camera_name"]
        

# Source - https://stackoverflow.com/a/77873699
# Posted by AKX, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-12, License - CC BY-SA 4.0

import requests

def download_with_wget(url : str, f : str) -> bool:
    cmd = f"wget -O {f} {url}"

    result = run_command(cmd)

    if result.returncode == 0:
        print(f"Successfully downloaded {url}")
        return True
    else:
        return False
    

def download_with_resume(sess: requests.Session, url: str, f):
    bytes_read = 0
    expected_length = None
    for attempt in range(10):
        if bytes_read:
            headers = {"Range": f"bytes={bytes_read}-"}
            expected_status = 206
        else:
            headers = {}
            expected_status = 200
        print(f"{url}: got {bytes_read} bytes...")
        resp = sess.get(url, stream=True, headers=headers, timeout=10)
        resp.raise_for_status()
        if resp.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {resp.status_code}")

        try:
            for chunk in resp.iter_content(chunk_size=None):
                f.write(chunk)
                bytes_read += len(chunk)
        except requests.exceptions.ChunkedEncodingError:
            pass
        except requests.exceptions.ConnectionError:
            pass

    if len(data) != expected_length:
        raise ValueError(f"Expected {expected_length} bytes, got {len(data)}")




  
    
def process_images(session):
    url = base_url + "/list/detail/backward/900000/60"
    thumb_url = base_url + "/thumb/"
    file_url = base_url + "/file/"
    delete_url = base_url + "/cmd/delete/"

    cam_reset(session)
    camera = get_cam_id(session)
    
    try:
        # 1. Send the GET request
        print(f"Sending {url}")
        response = session.get(url)
        
        # 2. Check if the request was successful (status code 200)
        # This raises an exception for 4XX or 5XX errors
        response.raise_for_status()

        # 3. Parse the JSON response into a Python dictionary or list
        data = response.json()

        images = data["data"]
        print(f"Received {url}; processing {len(images)} images")
        counter = 0
        for image in images:
            try:
                cam_reset(session)
                image_id = image["id"]
                image_date = image["date"]
                image_type = image["type"]
                filetype = "JPG" if image_type == 1 else "MP4"
                compressed_date = image_date.replace("-", "").replace(" ","").replace(":","")
                filename = f'{camera}_{compressed_date}_{image_id}.{filetype}'
                url = f'{file_url}{image_id}/{filetype}'
                print(url)
                response = session.get(url, stream=True)
#                with open(filename, "wb") as f:
#                    download_with_resume(session, url, f) 
                download_with_wget(url, filename) 
                response = session.get(f'{delete_url}{image_id}/{filetype}', timeout = 30)
                print(f'Received and deleted {filename}', flush=True)
                counter += 1
            except ChunkedEncodingError as chunk_err: # can get 0 bytes read - carry on, we can try again..
                print(f"A chunked encoding error occurred - carrying on but a file was not deleted: try again")

        # Example: If the JSON has a key named 'items'
        # for item in data.get('items', []):
        #     print(item)
        print(f'Total {counter} images/movies saved')
        return counter
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return -1
    except Exception as err:
        print(f"An error occurred: {err}")
        print(traceback.print_exc())
        return -1

def drop_wifi_linux(ssid):
    """Disconnect from WiFi on Linux."""
    cmd = f"nmcli c down {ssid}"
    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully dropped connection to {ssid}!")
        return True
    else:
        print(f"Failed to disconnect: {connect_result.stderr.strip()}")
        return False

def drop_wifi_macos(ssid):
    """Disconnect from WiFi on macOS by turning off Wi-Fi."""
    cmd = "sudo networksetup -setairportpower en0 off" 
    connect_result = run_command(cmd)
    """Disconnect from WiFi on macOS by making current not preferred."""
    cmd = f'sudo networksetup -removepreferredwirelessnetwork en0 {ssid}'
    connect_result = run_command(cmd)
    
    if connect_result.returncode == 0:
        print(f"Successfully dropped Wi-Fi connection!")
        time.sleep(2)  # Give airport time to power down
        return True
    else:
        print(f"Failed to disconnect: {connect_result.stderr.strip()}")
        return False

    return
    
def drop_wifi(ssid):
    """Platform-agnostic function to disconnect from WiFi."""
    if is_macos():
        return drop_wifi_macos(ssid)
    else:
        return drop_wifi_linux(ssid)

def restore_wifi_linux(ssid, devid):
    """Reconnect to WiFi on Linux."""
    cmd = f"nmcli c up {ssid}"
    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully connected to {ssid}!")
        return True
    else:
        print(f"Failed to connect: {connect_result.stderr.strip()}")
        return False

def restore_wifi_macos(ssid, devid):
    """Reconnect to WiFi on macOS by turning on Wi-Fi."""
    #    cmd = "sudo networksetup -setairportpower en0 on" 
    cmd = f'sudo networksetup -addpreferredwirelessnetworkatindex en0 {ssid} 1 wpa'

    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully restored Wi-Fi connection!")
        time.sleep(5)  # Give airport time to power up and scan
        return True
    else:
        print(f"Failed to connect: {connect_result.stderr.strip()}")
        return False

def restore_wifi(ssid, devid):
    """Platform-agnostic function to restore WiFi connection."""
    if is_macos():
        return restore_wifi_macos(ssid, devid)
    else:
        return restore_wifi_linux(ssid, devid)
    
        
def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Network Interface Configuration Script",
        epilog="Example: python script.py -p mySecretPassword --ssid MyHomeWiFi"
    )

    # --- Mandatory Arguments ---
    # We use 'required=True' to ensure the user provides the password
    parser.add_argument(
        "-p", "--password", 
        required=True, 
        help="The camera WiFi password (Mandatory)"
    )

    # --- Optional Arguments ---
    parser.add_argument(
        "-b", "--bt-id", 
        help="Bluetooth interface ID (e.g., hci0)"
    )

    # --- Optional Arguments ---
    parser.add_argument(
        "-d", "--device-id", 
        help="Bluetooth device ID (e.g., mac of remote bluetooth, or name)"
    )
    
    parser.add_argument(
        "-w", "--wifi-id", 
        help="WiFi interface ID (e.g., wlan0)"
    )
    
    parser.add_argument(
        "-s", "--ssid", 
        help="The existing WiFi SSID/Network name"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Accessing the values
    print(f"--- Configuration Received ---")
    print(f"WiFi Password: {args.password}")
    print(f"Bluetooth ID:  {args.bt_id if args.bt_id else 'Not provided'}")
    print(f"WiFi ID:       {args.wifi_id if args.wifi_id else 'Not provided'}")
    print(f"WiFi SSID:     {args.ssid if args.ssid else 'Not provided'}")


    if args.ssid:
        drop_wifi(args.ssid)

    asyncio.run(run(args.bt_id, args.device_id, args.wifi_id, args.password))
            
        
    if args.ssid:
        restore_wifi(args.ssid, args.wifi_id)
        


if __name__ == "__main__":
    main()    
