import sys
import os
import platform

def check_permissions():
    os_type = platform.system()
    
    if os_type == "Darwin":  # macOS
        import ctypes
        try:
            app_services = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')
            is_trusted = app_services.AXIsProcessTrusted()
            
            if not is_trusted:
                os.system("open 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'")
                sys.exit()
                
            print("macOS: İzinler onaylandı. Sistem hazır.")
        except Exception as e:
            print(f"macOS izin kontrolü sırasında hata: {e}")

    elif os_type == "Windows":
        import ctypes
        # Windows'ta kullanıcının yönetici (admin) haklarına sahip olup olmadığını kontrol ediyoruz
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("BİLGİ: Windows sisteminde özel bir izin ayarına gerek yoktur.")
            print("Ancak kısayol tuşu çalışmazsa, terminali/editörü 'Yönetici Olarak Çalıştır' (Run as Administrator) diyerek açmayı unutmayın.")
        else:
            print("Windows: Program yönetici haklarıyla çalışıyor. Sistem hazır.")

    elif os_type == "Linux":
        # Linux'ta modern Wayland sunucusu global tuşları engelleyebilir, bunu kontrol ediyoruz
        wayland_check = os.environ.get("WAYLAND_DISPLAY")
        if wayland_check:
            print("UYARI: Linux sisteminizde Wayland görüntü sunucusu aktif.")
            print("Wayland güvenlik mimarisi arka planda klavye dinlemeyi (pynput) engelleyebilir.")
            print("Eğer kısayol tuşu çalışmazsa, kodu 'sudo' ile çalıştırmayı veya oturumunuzu X11 (Xorg) ile açmayı deneyin.")
        else:
            print("Linux: X11 veya terminal ortamı algılandı. Sistem hazır.")
            
    else:
        print(f"Bilinmeyen bir işletim sistemi tespit edildi ({os_type}). İzin kontrolleri atlanıyor...")
