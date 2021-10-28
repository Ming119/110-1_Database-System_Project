*** Settings ***
Library    Selenium2Library
Resource    ../../Keywords/common.txt
Resource    ../../Keywords/flash.txt
Resource    ./UIR-04_Register.txt

Suite Setup    Run Keywords    Open Browser    ${webSiteURL}    ${browser}
...                     AND    Maximize Browser Window
...                     AND    Go to Register Page

Suite Teardown    Close Browser

*** Test Cases ***
