import ctypes
from ctypes import wintypes

# Constants from Windows API
SC_MANAGER_ALL_ACCESS = 0xF003F
SERVICE_ALL_ACCESS = 0xF01FF
SERVICE_DISABLED = 0x00000004

def Main(service_name : str):
    # Load the required libraries
    advapi32 = ctypes.WinDLL('advapi32.dll')

    # Define argument types and return types
    advapi32.OpenSCManagerW.argtypes = [
    wintypes.LPCWSTR,  # machine name
    wintypes.LPCWSTR,  # database name
    wintypes.DWORD     # access rights
    ]
    advapi32.OpenSCManagerW.restype = wintypes.SC_HANDLE

    advapi32.OpenServiceW.argtypes = [
    wintypes.SC_HANDLE,  # SCManager handle
    wintypes.LPCWSTR,    # service name
    wintypes.DWORD       # access rights
    ]
    advapi32.OpenServiceW.restype = wintypes.SC_HANDLE

    advapi32.ChangeServiceConfigW.argtypes = [
        wintypes.SC_HANDLE,  # service handle
        wintypes.DWORD,      # service type
        wintypes.DWORD,      # start type
        wintypes.DWORD,      # error control
        wintypes.LPCWSTR,    # binary path
        wintypes.LPCWSTR,    # load order group
        wintypes.LPDWORD,    # tag ID
        wintypes.LPCWSTR,    # dependencies
        wintypes.LPCWSTR,    # service start name
        wintypes.LPCWSTR,    # password
        wintypes.LPCWSTR     # display name
    ]
    advapi32.ChangeServiceConfigW.restype = wintypes.BOOL

    advapi32.CloseServiceHandle.argtypes = [wintypes.SC_HANDLE]
    advapi32.CloseServiceHandle.restype = wintypes.BOOL
    # Open the service control manager
    scm_handle = advapi32.OpenSCManagerW(None, None, SC_MANAGER_ALL_ACCESS)
    if not scm_handle:
        raise ctypes.WinError()
    
    try:
        # Open the service with SERVICE_ALL_ACCESS
        service_handle = advapi32.OpenServiceW(scm_handle, service_name, SERVICE_ALL_ACCESS)
        if not service_handle:
            raise ctypes.WinError()
        
        try:
            # Change the service configuration to disabled
            success = advapi32.ChangeServiceConfigW(
                service_handle,
                ctypes.c_uint32(0xFFFFFFFF),  # SERVICE_NO_CHANGE
                SERVICE_DISABLED,
                ctypes.c_uint32(0xFFFFFFFF),  # SERVICE_NO_CHANGE
                None, None, None, None, None, None, None
            )
            
            if not success:
                raise ctypes.WinError()
            
            print(f"Service '{service_name}' disabled successfully.")
            
        finally:
            advapi32.CloseServiceHandle(service_handle)
    finally:
        advapi32.CloseServiceHandle(scm_handle)

if __name__ == "__main__":
    blackcat1_drvname = "BlackCat1"
    Main(blackcat1_drvname)