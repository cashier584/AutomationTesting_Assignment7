# CONFIG
BASE_URL = "https://dailydictation.com"
USERNAME = "221130325@st.hcmuaf.edu.vn"
PASSWORD = "Vinh2004.."

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDailyDictation(unittest.TestCase):
    """Test suite - Login một lần, chạy tất cả tests liên tiếp"""
    
    @classmethod
    def setUpClass(cls):
        """Khởi tạo browser và login một lần duy nhất"""
        print("\n" + "="*60)
        print("→ Khởi tạo browser và đang nhập...")
        print("="*60)
        
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.vars = {}
        
        # Login
        print("→ Đang truy cập trang login...")
        cls.driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        try:
            username_field = WebDriverWait(cls.driver, 10).until(
                EC.presence_of_element_located((By.ID, "_username"))
            )
            username_field.clear()
            username_field.send_keys(USERNAME)
            time.sleep(0.5)
            
            password_field = cls.driver.find_element(By.ID, "_password")
            password_field.clear()
            password_field.send_keys(PASSWORD)
            time.sleep(0.5)
            
            submit_button = cls.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            time.sleep(2)
            
            WebDriverWait(cls.driver, 10).until(
                EC.url_changes(f"{BASE_URL}/login")
            )
            
            print("✓ Login thành công!")
            time.sleep(1)
            
        except Exception as e:
            print(f"✗ Login thất bại: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Đóng browser sau khi tất cả tests hoàn thành"""
        print("\n" + "="*60)
        print("→ Đóng browser...")
        print("="*60)
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """Trước mỗi test, quay về trang chủ và maximize window"""
        self.driver.maximize_window()
        self.driver.get(BASE_URL)
        time.sleep(1)

    # =============== TEST CASES ===============

    def test_EUP_EDITUSERNAME_SUCCESS_01(self):
        """Test 1: Edit username thành công"""
        print("\n→ Test 1: Edit username thành công")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Account information").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/user/edit-display-name"]').click()
        time.sleep(0.5)
        display_name_field = self.driver.find_element(By.ID, "edit_display_name_displayName")
        display_name_field.clear()
        time.sleep(0.5)
        display_name_field.send_keys("Vinh2123")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "edit_display_name_submit").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "View profile").click()
        time.sleep(0.5)
        element = self.driver.find_element(By.LINK_TEXT, "Edit")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def test_EUP_EDITUSERNAME_EMPTY_02(self):
        """Test 2: Edit username với giá trị empty"""
        print("\n→ Test 2: Edit username với giá trị empty")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Account information").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/user/edit-display-name"]'))
        )
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/user/edit-display-name"]').click()
        time.sleep(0.5)
        display_name_field = self.driver.find_element(By.ID, "edit_display_name_displayName")
        display_name_field.clear()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "edit_display_name_submit").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".invalid-feedback"))
        )
        assert self.driver.find_element(By.CSS_SELECTOR, ".invalid-feedback").text == "This value should not be blank."

    def test_EUP_EDITUSERNAME_SPECIALCHAR_03(self):
        """Test 3: Edit username với special characters"""
        print("\n→ Test 3: Edit username với special characters")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Account information").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/user/edit-display-name"]').click()
        time.sleep(0.5)
        display_name_field = self.driver.find_element(By.ID, "edit_display_name_displayName")
        display_name_field.clear()
        time.sleep(0.5)
        display_name_field.send_keys("abc@@@@@")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "edit_display_name_submit").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "View profile").click()
        time.sleep(0.5)
        element = self.driver.find_element(By.LINK_TEXT, "Edit")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def test_EUP_CHANGEPASSWORD_SUCCESS_04(self):
        """Test 4: Change password thành công"""
        print("\n→ Test 4: Change password thành công")
        # Mở dropdown menu
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".d-md-inline"))
        )
        dropdown.click()
        time.sleep(0.5)
        # Click vào Change password
        change_pass_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Change password"))
        )
        change_pass_link.click()
        time.sleep(0.5)
        current_password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "change_password_currentPassword"))
        )
        current_password_field.send_keys("Vinh2004..")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").send_keys("Vinh2004@@")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_submit").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text == "Your password has been updated."
        
        # Đổi password về lại ban đầu để các test sau không bị ảnh hưởng
        time.sleep(1)
        dropdown2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".d-md-inline"))
        )
        dropdown2.click()
        time.sleep(0.5)
        change_pass_link2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Change password"))
        )
        change_pass_link2.click()
        time.sleep(0.5)
        current_password_field2 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "change_password_currentPassword"))
        )
        current_password_field2.send_keys("Vinh2004@@")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").send_keys("Vinh2004..")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_submit").click()
        time.sleep(0.5)

    def test_EUP_CHANGEPASSWORD_WRONG_OLD_05(self):
        """Test 5: Change password với old password sai"""
        print("\n→ Test 5: Change password với old password sai")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Change password").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_currentPassword").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_currentPassword").send_keys("Vinh652371")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_newPassword").send_keys("Vhuinaksbd87623")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "change_password_submit").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".invalid-feedback"))
        )
        assert self.driver.find_element(By.CSS_SELECTOR, ".invalid-feedback").text == "Incorrect value"

    def test_EUP_CHANGE_EMAIL_SUCCESS_06(self):
        """Test 6: Change email thành công"""
        print("\n→ Test 6: Change email thành công")
        self.driver.find_element(By.ID, "account-dropdown-toggle").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Change Email").click()
        time.sleep(0.5)
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "edit_email_email"))
        )
        email_field.clear()
        time.sleep(0.5)
        email_field.send_keys("congvinh@gmail.com")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "edit_email_submit").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text == "Your email has been updated!"

    def test_VP_VIEW_PROGRESS_SUMMARY_07(self):
        """Test 7: View progress summary"""
        print("\n→ Test 7: View progress summary")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Public profile").click()
        time.sleep(0.8)
        assert self.driver.find_element(By.XPATH, "//span[normalize-space()='Lesson completions:']").text == "Lesson completions:"
        assert self.driver.find_element(By.XPATH, "//span[normalize-space()='Active days:']").text == "Active days:"
        assert self.driver.find_element(By.XPATH, "//span[normalize-space()='Active time:']").text == "Active time:"

    def test_VP_VIEW_PROGRESS_ACTIVITY_08(self):
        """Test 8: View progress activity"""
        print("\n→ Test 8: View progress activity")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Public profile").click()
        time.sleep(0.8)
        self.driver.find_element(By.XPATH, "//button[contains(., 'View recent lessons')]").click()
        time.sleep(1)
        lesson_elements = self.driver.find_elements(By.XPATH, "//ul[@class='list-group']//a")
        assert len(lesson_elements) > 0, "Không tìm thấy lesson nào trong danh sách"

    def test_VP_VIEW_PROGRESS_STAR_09(self):
        """Test 9: View progress star"""
        print("\n→ Test 9: View progress star")
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Public profile").click()
        time.sleep(0.8)
        self.driver.find_element(By.XPATH, "//button[contains(., 'View recent lessons')]").click()
        time.sleep(1)
        lesson_elements = self.driver.find_elements(By.XPATH, "//ul[@class='list-group']//a")
        assert len(lesson_elements) > 0, "Không tìm thấy lesson nào trong danh sách"
        star_elements = self.driver.find_elements(By.XPATH, "//i[contains(@class,'bi-star-fill')]")
        if len(star_elements) > 0:
            attribute = star_elements[0].get_attribute("aria-label")
            self.vars["starLabel"] = attribute
            assert attribute is not None, "Không tìm thấy aria-label của star"

    def test_UPAL_UPDATE_PROGRESS_10(self):
        """Test 10: Update progress"""
        print("\n→ Test 10: Update progress")
        self.driver.find_element(By.LINK_TEXT, "All exercises").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Conversations").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "#groupsAccordion103 .fw-bolder").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "#lessonGroup103 .col-lg-4:nth-child(1) > .bg-body-tertiary:nth-child(1) .fw-semibold:nth-child(1)").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "dictationInput").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "dictationInput").send_keys("It depends on the season. Anywhere from one month to two months.")
        time.sleep(0.5)
        self.driver.find_element(By.ID, "btn-check").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".d-md-inline").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Public profile").click()
        time.sleep(0.5)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".text-decoration-underline"))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".text-decoration-underline").click()
        time.sleep(0.5)


if __name__ == '__main__':
    # Chạy tests
    unittest.main(verbosity=2)
