import os
import Vision
from Foundation import NSURL
import mss

def process_with_apple_vision(img_path, selected_region):
    
    print("Apple Vision ile metin ve koordinatlar analiz ediliyor...")
    
    # mss ile sadece seçilen alanın SS'ini al ve diske kaydet (Vision dosya okumayı sever)
    with mss.mss() as sct:
        sct_img = sct.grab(selected_region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=img_path)

    # Apple Vision API'yi çağır
    url = NSURL.fileURLWithPath_(img_path)
    request_handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)

    success, error = request_handler.performRequests_error_([request], None)

    if success:
        results = request.results()
        if not results:
            print("Metin bulunamadı.")
            return

        print("\n--- BULUNAN METİNLER VE TAM KONUMLARI ---")
        for observation in results:
            text = observation.topCandidates_(1)[0].string()
            
            # Apple Vision'dan gelen (0.0 - 1.0) yüzdelik koordinat kutusu
            bbox = observation.boundingBox()
            
            # 1. Aşama: Kutuyu yerel piksel boyutuna çevirme (Y ekseni Apple'da alttan başlar, onu ters çeviriyoruz)
            local_x = int(bbox.origin.x * selected_region["width"])
            local_y = int((1.0 - bbox.origin.y - bbox.size.height) * selected_region["height"])
            text_w = int(bbox.size.width * selected_region["width"])
            text_h = int(bbox.size.height * selected_region["height"])
            
            # 2. Aşama: Ekrandaki mutlak (Global) konumu bulma
            global_x = selected_region["left"] + local_x
            global_y = selected_region["top"] + local_y
            
            print(f"Metin: '{text}'")
            print(f"Konum -> X: {global_x}, Y: {global_y} (Genişlik: {text_w}, Yükseklik: {text_h})")
            print("-" * 40)
            
            # İşte tam bu 'global_x' ve 'global_y' değerlerini bir sonraki aşamada 
            # PyQt6 ile Türkçe çeviriyi ekrana basarken kullanacağız!

    else:
        print("Vision Hatası:", error)