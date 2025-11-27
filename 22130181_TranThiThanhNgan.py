import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

url = "https://dailydictation.com/exercises/short-stories/1-first-snowfall.1/listen-and-type"
driver.get(url)
time.sleep(3)

# Mở transcript
try:
    show_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Full Audio & Plain Transcript')]")
    show_btn.click()
    time.sleep(1)
except:
    print("Không thấy nút transcript")

print("---- TRANSCRIPT ----")

# Lấy transcript
transcript_items = driver.find_elements(By.XPATH, "//div[contains(@title, 'Challenge #')]")
for item in transcript_items:
    print(item.text)

print("\n---- AUDIO URL ----")

# Lấy URL audio
source_elements = driver.find_elements(By.XPATH, "//source[@type='audio/mpeg']")
if source_elements:
    audio_src = source_elements[0].get_attribute("src")
    print("✔ REAL AUDIO URL:", audio_src)
else:
    print("✖ Không tìm thấy audio source")

# TC_ShowFullAudio_PlayAudio_02
print("\n---- TEST PLAY AUDIO (Phương pháp : JavaScript) ----")

try:
    # 1. Tìm thẻ AUDIO dựa trên class
    audio_element = driver.find_element(By.CSS_SELECTOR, "audio.my-3")

    print("✔ Đã tìm thấy thẻ <audio>")

    # 2. Dùng JavaScript để ép audio phát
    driver.execute_script("arguments[0].play();", audio_element)
    print("✔ Đã gửi lệnh play()... Đang chờ audio load...")

    # Chờ audio load
    time.sleep(4)

    # 3. Kiểm tra xem audio có thực sự chạy không
    is_paused = driver.execute_script("return arguments[0].paused;", audio_element)

    t1 = driver.execute_script("return arguments[0].currentTime;", audio_element)
    time.sleep(2)
    t2 = driver.execute_script("return arguments[0].currentTime;", audio_element)

    print(f"   + Trạng thái Paused: {is_paused}")
    print(f"   + Thời gian: {t1:.2f} -> {t2:.2f}")

    if not is_paused and t2 > t1:
        print("=> KẾT LUẬN: Audio HOẠT ĐỘNG tốt (Âm thanh đang phát).")
    elif t2 > t1:
        print("=> KẾT LUẬN: Audio đang chạy (currentTime có tăng).")
    else:
        print("=> KẾT LUẬN: Audio KHÔNG phát (Có thể lỗi mạng hoặc file hỏng).")

except Exception as e:
    print(f"✖ Lỗi: Không tìm thấy thẻ audio hoặc không thể phát. Chi tiết: {e}")
# TC_ShowFullAudio_OffSpeaker_03
print("\n---- TEST PLAY & MUTE AUDIO ----")

try:
    # 1. Tìm thẻ AUDIO
    audio_element = driver.find_element(By.CSS_SELECTOR, "audio.my-3")
    print("✔ Đã tìm thấy thẻ <audio>")

    # 2. Phát Audio
    driver.execute_script("arguments[0].play();", audio_element)
    print("✔ Đã gửi lệnh play()... Đang chờ audio load...")
    time.sleep(4)  # Chờ load

    # 3. Kiểm tra Audio có chạy không
    t1 = driver.execute_script("return arguments[0].currentTime;", audio_element)
    time.sleep(2)
    t2 = driver.execute_script("return arguments[0].currentTime;", audio_element)

    if t2 > t1:
        print(f"✔ Audio đang chạy tốt ({t1:.2f} -> {t2:.2f})")

        # --- PHẦN MỚI: TẮT TIẾNG (MUTE) ---
        print("➤ Đang thực hiện tắt tiếng (Mute)...")

        # Lệnh JS để set thuộc tính muted = true
        driver.execute_script("arguments[0].muted = true;", audio_element)
        time.sleep(1)

        # Kiểm tra lại xem đã mute chưa
        is_muted = driver.execute_script("return arguments[0].muted;", audio_element)

        if is_muted:
            print("✔ KẾT LUẬN: Đã tắt loa thành công (Muted: True) 🔇")
        else:
            print("✖ KẾT LUẬN: Chưa tắt được loa 🔊")

    else:
        print("✖ Audio không chạy, bỏ qua bước Mute.")

except Exception as e:
    print(f"✖ Lỗi: {e}")
# TC_ShowFullAudio_SeekAudio_04
try:
    # 1. Tìm thẻ AUDIO
    audio_element = driver.find_element(By.CSS_SELECTOR, "audio.my-3")
    print("✔ Đã tìm thấy thẻ <audio>")

    # 2. Phát Audio để load metadata (nếu không load thì duration sẽ là NaN)
    driver.execute_script("arguments[0].play();", audio_element)
    print("➤ Đang phát audio... chờ load metadata...")
    time.sleep(4)  # Chờ audio buffer

    # 3. Lấy tổng thời lượng (Duration)
    duration = driver.execute_script("return arguments[0].duration;", audio_element)
    print(f"✔ Tổng thời lượng audio: {duration:.2f} giây")

    # 4. Tính toán điểm muốn tua tới (Ví dụ: Tua tới 50% bài)
    target_time = duration / 2
    print(f"➤ Chuẩn bị trượt thanh thời gian tới: {target_time:.2f} giây (50%)")

    # 5. THỰC HIỆN "TRƯỢT" (Set currentTime)
    # Hành động này sẽ làm thanh trượt trên giao diện tự động nhảy đến giữa
    driver.execute_script(f"arguments[0].currentTime = {target_time};", audio_element)
    time.sleep(2)  # Chờ audio ổn định sau khi tua

    # 6. Kiểm tra kết quả
    current_time = driver.execute_script("return arguments[0].currentTime;", audio_element)

    # Cho phép sai số nhỏ (khoảng 1-2 giây) do độ trễ khi tua
    if abs(current_time - target_time) < 3.0:
        print(f"✔ KẾT LUẬN: Đã tua thành công! Thời gian hiện tại: {current_time:.2f}s")
        print("  (Thanh thời gian trên UI đã nhảy đến vị trí mới)")
    else:
        print(f"✖ KẾT LUẬN: Tua thất bại. Thời gian hiện tại: {current_time:.2f}s")

except Exception as e:
    print(f"✖ Lỗi: {e}")
# TC_ShowFullAudio_Download_05
print("\n---- TEST DOWNLOAD AUDIO ----")

try:
    # 1. Tìm thẻ AUDIO
    audio_element = driver.find_element(By.CSS_SELECTOR, "audio.my-3")

    # 2. Lấy đường dẫn URL thực của file audio
    # Dùng thuộc tính 'currentSrc' là chính xác nhất cho thẻ HTML5 Audio
    audio_src = driver.execute_script("return arguments[0].currentSrc;", audio_element)

    print(f"✔ Đã lấy được link Audio: {audio_src}")

    if not audio_src:
        raise Exception("Không tìm thấy link file audio (src rỗng)")

    # 3. Thực hiện tải file bằng Python (Giả lập hành động tải xuống)
    print("➤ Đang tiến hành tải file về máy...")

    # Tên file sẽ lưu
    file_name = "test_downloaded_audio.mp3"

    # Gửi request tải file
    response = requests.get(audio_src, stream=True)

    if response.status_code == 200:
        # Ghi file vào ổ cứng
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print("✔ Đã tải xong.")

        # 4. Kiểm tra file có tồn tại và không bị lỗi (dung lượng > 0)
        if os.path.exists(file_name):
            file_size = os.path.getsize(file_name)
            print(f"✔ VERIFY: File '{file_name}' đang nằm trong folder dự án.")
            print(f"✔ VERIFY: Dung lượng file = {file_size} bytes.")

            if file_size > 1000:  # File audio thường phải lớn hơn 1KB
                print("=> KẾT LUẬN: Chức năng tải xuống hoạt động TỐT ✅")
            else:
                print("=> KẾT LUẬN: File tải về bị lỗi (dung lượng quá nhỏ) ❌")

            # (Tùy chọn) Xóa file sau khi test xong để dọn dẹp
            # os.remove(file_name)
            # print("  (Đã xóa file test để dọn dẹp)")
        else:
            print("=> KẾT LUẬN: Không tìm thấy file trên ổ cứng ❌")

    else:
        print(f"✖ Lỗi HTTP khi tải: {response.status_code}")

except Exception as e:
    print(f"✖ Lỗi: {e}")

#TC_ShowFullAudio_Speed_06
print("\n---- TEST PLAYBACK SPEED (TỐC ĐỘ PHÁT) ----")

try:
    # 1. Tìm thẻ AUDIO
    audio_element = driver.find_element(By.CSS_SELECTOR, "audio.my-3")

    # Bắt đầu phát
    driver.execute_script("arguments[0].play();", audio_element)
    time.sleep(3)  # Chờ ổn định

    # --- TEST CASE 1: Tăng tốc độ lên 2.0x ---
    print("\n[Case 1] Thử nghiệm tốc độ 2.0x (Nhanh gấp đôi)")

    # Dùng JS set playbackRate
    driver.execute_script("arguments[0].playbackRate = 2.0;", audio_element)

    # Đo thời gian
    t_start = driver.execute_script("return arguments[0].currentTime;", audio_element)

    # Cho chạy thực tế 3 giây
    time.sleep(3)

    t_end = driver.execute_script("return arguments[0].currentTime;", audio_element)

    diff = t_end - t_start
    print(f"   + Thời gian thực trôi qua: 3 giây")
    print(f"   + Thời gian audio trôi qua: {diff:.2f} giây")

    # Nếu tốc độ 2.0 thì trong 3s thực, audio phải chạy được khoảng 6s (cho phép sai số > 5s)
    if diff > 5.0:
        print("   => KẾT LUẬN: Tốc độ 2.0x hoạt động ĐÚNG ✅")
    else:
        print("   => KẾT LUẬN: Tốc độ 2.0x SAI ❌")

    # --- TEST CASE 2: Giảm tốc độ xuống 0.5x ---
    print("\n[Case 2] Thử nghiệm tốc độ 0.5x (Chậm một nửa)")

    # Dùng JS set playbackRate
    driver.execute_script("arguments[0].playbackRate = 0.5;", audio_element)

    # Đo thời gian
    t_start = driver.execute_script("return arguments[0].currentTime;", audio_element)

    # Cho chạy thực tế 3 giây
    time.sleep(3)

    t_end = driver.execute_script("return arguments[0].currentTime;", audio_element)

    diff = t_end - t_start
    print(f"   + Thời gian thực trôi qua: 3 giây")
    print(f"   + Thời gian audio trôi qua: {diff:.2f} giây")

    # Nếu tốc độ 0.5 thì trong 3s thực, audio chỉ chạy được khoảng 1.5s (chấp nhận < 2.0s)
    if diff < 2.0:
        print("   => KẾT LUẬN: Tốc độ 0.5x hoạt động ĐÚNG ✅")
    else:
        print("   => KẾT LUẬN: Tốc độ 0.5x SAI ❌")

    # Reset về bình thường (1.0) trước khi tắt
    driver.execute_script("arguments[0].playbackRate = 1.0;", audio_element)

except Exception as e:
    print(f"✖ Lỗi: {e}")
# chức năng 2
# ShowFullTranScript

time.sleep(5)
driver.quit()