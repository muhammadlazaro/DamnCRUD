import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver import create_driver

import os

BASE_URL = os.getenv("BASE_URL", "http://localhost/DamnCRUD")


# =========================
# FIXTURE SETUP
# =========================

@pytest.fixture(scope="function")
def driver():
    driver = create_driver()
    driver.maximize_window()
    yield driver
    driver.quit()


def login(driver):
    driver.get(f"{BASE_URL}/login.php")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("index.php")
    )


# =========================
# FT_006 - Add Contact Valid
# =========================

def test_FT_006_add_contact_valid(driver):
    login(driver)

    driver.find_element(By.LINK_TEXT, "Add New Contact").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )

    driver.find_element(By.NAME, "name").send_keys("Selenium Tester")
    driver.find_element(By.NAME, "email").send_keys("selenium@test.com")
    driver.find_element(By.NAME, "phone").send_keys("081234567890")
    driver.find_element(By.NAME, "title").send_keys("Tester")

    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("index.php")
    )

    assert "Selenium Tester" in driver.page_source


# =========================
# FT_008 - Edit Contact
# =========================

def test_FT_008_edit_contact(driver):
    login(driver)

    # Pastikan ada tombol edit
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn-success"))
    )

    edit_buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn-success")
    assert len(edit_buttons) > 0, "Tidak ada data untuk diedit"

    edit_buttons[0].click()

    # Tunggu form muncul
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )

    # Ambil semua field required
    name = driver.find_element(By.NAME, "name")
    email = driver.find_element(By.NAME, "email")
    phone = driver.find_element(By.NAME, "phone")
    title = driver.find_element(By.NAME, "title")

    # Pastikan tidak ada field kosong (hindari HTML5 validation error)
    if name.get_attribute("value") == "":
        name.send_keys("Selenium User")

    if email.get_attribute("value") == "":
        email.send_keys("selenium@email.com")

    if phone.get_attribute("value") == "":
        phone.send_keys("081234567890")

    # Update title
    title.clear()
    title.send_keys("Updated Title")

    # Submit
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Tunggu kembali ke index
    WebDriverWait(driver, 10).until(
        EC.url_contains("index.php")
    )

    # Verifikasi perubahan tampil
    assert "Updated Title" in driver.page_source


# =========================
# FT_009 - Delete Contact
# =========================

def test_FT_009_delete_contact_confirm(driver):
    login(driver)

    # Tunggu tabel muncul
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#employee tbody tr"))
    )

    # Ambil baris paling atas
    first_row = driver.find_element(By.CSS_SELECTOR, "#employee tbody tr")

    # Ambil nama baris paling atas (kolom ke-2)
    first_name = first_row.find_elements(By.TAG_NAME, "td")[1].text

    # Klik tombol delete di baris paling atas
    delete_button = first_row.find_element(By.CSS_SELECTOR, "a.btn-danger")
    delete_button.click()

    # Tunggu popup muncul
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    # Tunggu sampai baris pertama berubah
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#employee tbody tr")
                 .find_elements(By.TAG_NAME, "td")[1].text != first_name
    )

    # Pastikan nama lama sudah tidak ada
    assert first_name not in driver.page_source


# =========================
# FT_016 - Search Not Found
# =========================

def test_FT_016_search_not_found(driver):
    login(driver)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.dataTables_filter input")
        )
    )

    search_box = driver.find_element(
        By.CSS_SELECTOR, "div.dataTables_filter input"
    )

    search_box.clear()
    search_box.send_keys("zzzzzzzznotfound")

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#employee tbody"),
            "No matching records found"
        )
    )

    assert "No matching records found" in driver.page_source


# =========================
# FT_019 - Upload Invalid File
# =========================

def test_FT_019_upload_invalid_photo(driver):
    login(driver)

    driver.get(f"{BASE_URL}/profil.php")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    file_path = os.path.abspath("test_files/test.pdf")

    upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload.send_keys(file_path)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    assert "Ekstensi tidak diijinkan" in driver.page_source