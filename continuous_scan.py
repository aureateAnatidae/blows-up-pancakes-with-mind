import asyncio
import nest_asyncio
nest_asyncio.apply()

import logging
   
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


async def cont_scan(timeout:int=16, refresh:int=2, *grep:str):
    '''
    Every <refresh> seconds, return all detected BT devices as list of class BLEDevice objects
    //device means MAC addresses + device name
    
    Parameters
    ----------
    timeout : int, default=16
        after <timeout> seconds, the scan stops refreshing
    refresh : int, default=2
        how long to wait in seconds before returning detected BT devices
    *grep : str, optional
        (optional) return only devices containing this string in name or MAC address
    
    Returns
    -------
    devices : list of object
        list containing all detected BLEDevices
        
    Raises
    ------
    bleak
        unable to connect with bleak
    '''
    
    stop_event = asyncio.Event()
        
    def callback(device, advertisement_data):
        print("i smell a device!")
        print(device)
        return device

    
    async with BleakScanner(callback) as scanner:
        #await scanner.discover(timeout=refresh)
        await asyncio.sleep(refresh)
        stop_event.set()

if __name__ == '__main__':
    asyncio.run(cont_scan())

    
    