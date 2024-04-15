********************************************************************************************************************
*******************WASHINGTON DRIVERS LICENSE GENERATOR*************************************************************
********************************************************************************************************************
***************************************Version 1.0******************************************************************
********************************************************************************************************************
***I have not implimented the automation of entering the photos or the signature************************************
********************************************************************************************************************
***that is comming in version 1.1 in the next day or two************************************************************
********************************************************************************************************************
***VERSION 2.0 will feature a fully complianyt AAMVA barcode that will be generated at the time of submition and ***
***along with the front ID overlay it will generate the entire back of the card as well as the front****************
********************************************************************************************************************
********************************************************************************************************************
***final version will include an option to have the images created as reverse transfer images or direct to card*****
********************************************************************************************************************
********************************************************************************************************************

first things first this is 100% written in Python so make you have a good environment installed.

this will be for a typical windows explanation, my friend who i had in mind runs windows and if your running linux, 
you ought to already know this and if your on an apple....oops!  it will work just fine, just REALLY, i get its BSD
based but why you wanna run proprietary soft that is and should be GNU Not Unix free and Open Source!

1.) press windows key, type cmd.exe, right click "run as administrator"

2.) your teminal screen ought to look like this:

        C:\windows\system32>   

    now copy and paste this into the terminal and press enter.   wait for screen to return to a blinking cursor on a line like above    

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

3.) Now type or copy and paste:

chocolatey install inkscape

press enter

follow the prompts choose a for all and press enter

when that completes now type:

chocolatey install python

press enter

next type pip install -r requirements.txt

now go to the WaIdTemp folder

cd c:\Users\****your_user_name*****\Downloads\WaIdTemp 

enter but substitue your actual username for ****your_user_name*****   

this is a typical path to your Downloads folder if different cd into where you put it.

now type python WAIDmod_V1.0_by_g1l34t20n.py 

press enter , wait abouy 20-30 seconds before cussing me out its a big csv and i havent optomized the script for speed

a box will appear fill in the details as you wish hit "generate license"

you will now have a new csv file in the WaIdTemp folder with my program.

enjoy!!!!!!!

g1l34t20n






