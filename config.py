import os

import pydantic
from appium.options.android import UiAutomator2Options
from typing import Literal, Optional
from dotenv import load_dotenv

EnvContext = Literal['personal', 'test', 'stage', 'prod']


class Settings(pydantic.BaseSettings):
    context: EnvContext = 'personal'

    # --- Appium Capabilities ---
    platformName: str = 'android'
    platformVersion: str = '9.0'
    deviceName: str = 'Google Pixel 3'
    app: Optional[str] = None
    appName: Optional[str] = None

    # --- > BrowserStack Capabilities ---
    projectName: Optional[str] = None
    buildName: Optional[str] = None
    sessionName: Optional[str] = None
    # --- > > BrowserStack credentials---
    userName: Optional[str] = None
    accessKey: Optional[str] = None

    # --- Remote Driver ---
    load_dotenv()
    remote_url: str = os.getenv('REMOTE_URL')

    # --- Selene ---
    timeout: float = 6.0

    @property
    def driver_options(self):
        load_dotenv()
        options = UiAutomator2Options()
        options.device_name = self.deviceName
        options.platform_name = self.platformName
        options.app = self.app
        if 'hub.browserstack.com' in self.remote_url:
            options.load_capabilities(
                {
                    'platformVersion': self.platformVersion,
                    'bstack:options': {
                        'projectName': os.getenv('PROJECTNAME'),
                        'buildName': os.getenv('BUILDNAME'),
                        'sessionName': os.getenv('SESSIONNAME'),
                        'userName': os.getenv('USER_NAME'),
                        'accessKey': os.getenv('ACCESSKEY'),
                    },
                }
            )

        return options


settings = Settings()


