#!/usr/bin/python
import traceback
import requests
from requests.exceptions import HTTPError, ChunkedEncodingError
import argparse

import asyncio
import sys
from bleak import BleakClient

# Define the UUIDs based on your service/characteristic shorthand
# Note: Full 128-bit UUIDs are often required if these are custom
#SERVICE_UUID = 
CHAR_UUID    = "0000ffb1-0000-1000-8000-00805f9b34fb"

async def run(bt_local_id, address):
    print(f"Searching for and connecting to {address}...")
    
    try:
        async with BleakClient(address, adapter=bt_local_id, timeout=30.0) as client:
            if client.is_connected:
                print(f"Connected to {address}")
                
                # Convert text payload to bytes
                payload = "TCWAKEUP".encode('utf-8')
                
                print(f"Sending payload to {CHAR_UUID}...")
                # write_gatt_char sends data to the device
                await client.write_gatt_char(CHAR_UUID, payload)
                
                print("Payload sent successfully.")
                return True
            else:
                print(f"Failed to connect to {address}")
                return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

import subprocess
import time
import sys

def run_command(command):
    """Helper to run shell commands and return output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

def connect_to_cam_wifi(device, password=None):

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
            return

        # Split output into a list of SSIDs and filter for those starting with 'CAM'
        ssids = scan_result.stdout.strip().split('\n')
        target_ssid = next((s for s in ssids if s.startswith("CAM")), None)
        
        if not target_ssid:
            print(f"No Wi-Fi network starting with 'CAM' was found (retry {retry}).")
            print(scan_result.stdout)
        else:
            break

    if not target_ssid:
        return
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
        
base_url = "http://192.168.8.1:8080"


def cam_reset():
    reset_url = base_url + "/cmd/standby/reset"
    try:
        response = requests.get(reset_url)
        data = response.json()
        
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        print(traceback.print_exc())
    
def get_cam_id():
    info_url = base_url + "/cmd/getSetting"
    try:
        response = requests.get(info_url)
        data = response.json()
        return data["data"]["camera_name"]
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        print(traceback.print_exc())
        
    
    
def process_images():
    url = base_url + "/list/detail/backward/900000/60"
    thumb_url = base_url + "/thumb/"
    file_url = base_url + "/file/"
    delete_url = base_url + "/cmd/delete/"

    cam_reset()
    camera = get_cam_id()
    
    try:
        # 1. Send the GET request
        response = requests.get(url)
        
        # 2. Check if the request was successful (status code 200)
        # This raises an exception for 4XX or 5XX errors
        response.raise_for_status()

        # 3. Parse the JSON response into a Python dictionary or list
        data = response.json()

        images = data["data"]
        counter = 0
        for image in images:
            try:
                image_id = image["id"]
                image_date = image["date"]
                image_type = image["type"]
                filetype = "JPG" if image_type == 1 else "MP4"
                compressed_date = image_date.replace("-", "").replace(" ","").replace(":","")
                filename = f'{camera}_{compressed_date}_{image_id}.{filetype}'
                thumbname = f'{camera}_{compressed_date}_{image_id}_thumb.{filetype}'
                
                response = requests.get(f'{thumb_url}{image_id}/{filetype}')
                with open(thumbname, "wb") as f:
                    f.write(response.content)
                    response = requests.get(f'{file_url}{image_id}/{filetype}')
                with open(filename, "wb") as f:
                    f.write(response.content)
                cam_reset()
                response = requests.get(f'{delete_url}{image_id}/{filetype}')
                print(f'Received and deleted {filename}', flush=True)
                counter += 1
            except ChunkedEncodingError as chunk_err: # can get 0 bytes read - carry on, we can try again..
                print(f"A chunked encoding error occurred - carrying on but a file was not deleted: try again")
        # Example: If the JSON has a key named 'items'
        # for item in data.get('items', []):
        #     print(item)
        print(f'Total {counter} images/movies saved')

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        print(traceback.print_exc())

        
def drop_wifi(ssid):
    cmd = f"nmcli c down {ssid}"

    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully dropped connection to {ssid}!")
    else:
        print(f"Failed to disconnect: {connect_result.stderr.strip()}")
        sys.exit(1)


def restore_wifi(ssid, devid):
    cmd = f"nmcli c up {ssid}"

    connect_result = run_command(cmd)

    if connect_result.returncode == 0:
        print(f"Successfully connected to {ssid}!")
    else:
        print(f"Failed to connect: {connect_result.stderr.strip()}")
        sys.exit(1)
    
        
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

    if asyncio.run(run(args.bt_id, args.device_id)):
        if connect_to_cam_wifi(args.wifi_id, args.password):
            process_images()
            
        
    if args.ssid:
        restore_wifi(args.ssid, args.wifi_id)
        


if __name__ == "__main__":
    main()    
