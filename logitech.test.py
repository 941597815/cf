from pefile import PE

def list_functions_from_dll(dll_path):
    pe = PE(dll_path)
    for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        print(export.name.decode())

dll_path = 'logitech.driver.dll'  # 替换为实际的 DLL 文件路径
list_functions_from_dll(dll_path)