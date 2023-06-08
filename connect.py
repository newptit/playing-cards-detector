from appium import webdriver


def connect_appium():
    desired_caps = {
        "appium:uuid": "eead0fc1",
        "platformName": "Android",
        # Add other desired capabilities such as appPackage and appActivity if required
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver;