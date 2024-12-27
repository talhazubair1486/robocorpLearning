from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    #browser.configure(
        #slowmo=100
    #)
    #open_robot_order_website()
    #close_annoying_modal()
    #orders = get_orders()
    #fill_the_form(orders)
    archive_receipts()
    
def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    """download orders file, read it as a table, return the result"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

    library = Tables()
    table = library.read_table_from_csv("orders.csv")
    return table

def close_annoying_modal():
    page = browser.page()
    page.click("text=OK")

def fill_the_form(orders):
    for row in orders:
        page = browser.page()
        page.select_option("#head", row["Head"])
        body_value = row["Body"]
        page.click(f"#id-body-{body_value}")
        page.fill(".form-control", row["Legs"])
        page.fill("#address", row["Address"])
        page.click("text=Preview")
        page.click("#order")
        page = browser.page()         
        if page.query_selector(".alert.alert-danger"):
            page.click("#order")
        if page.query_selector(".alert.alert-danger"):
            page.click("#order")
        if page.query_selector(".alert.alert-danger"):
            page.click("#order")
        if page.query_selector(".alert.alert-danger"):
            page.click("#order")
        page = browser.page()
        embed_screenshot_to_receipt(screenshot_robot(row["Order number"]), store_receipt_as_pdf(row["Order number"]))
        page.click("text=Order another robot")
        close_annoying_modal()

def store_receipt_as_pdf(order_number):
    pdf = PDF()

    page = browser.page()
    order_receipt_html = page.locator("#receipt").inner_html()

    path = f"output\\reciepts\order_receipt_{order_number}.pdf"
    pdf.html_to_pdf(order_receipt_html, path)
   
    return path

def screenshot_robot(orderNum):
    page = browser.page()
    screenshot_path = f"output\screenshot{orderNum}.png"
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path



def embed_screenshot_to_receipt(screenshot, pdf_file):
    pdf = PDF()
    print(f"screenshot path1: {screenshot}")
    print(f"pdf file: {pdf_file}")
    pdf.add_files_to_pdf(files=[screenshot],target_document=pdf_file, append=True)

def archive_receipts():
    lib = Archive()
    lib.archive_folder_with_zip("output/reciepts", "myreceipts.zip")