from pathlib import Path



class UIInspector:

    def __init__(self, driver):

        self.driver = driver

    # ----------------------------------------
    # Capture Current Screen XML
    # ----------------------------------------

    def capture_page_source(self):

        xml = self.driver.page_source

        output = (
            Path(__file__).resolve().parent.parent
            / "artifacts"
            / "screen.xml"
        )

        output.parent.mkdir(
            exist_ok=True
        )

        output.write_text(
            xml,
            encoding="utf-8"
        )

        print(f"\n✅ Page Source Saved\n{output}")

        return output




# Reuse driver from conftest
if __name__ == "__main__":
        from tests.conftest import get_driver

        driver = get_driver()

        inspector = UIInspector(driver)

        inspector.capture_page_source()

        driver.quit()