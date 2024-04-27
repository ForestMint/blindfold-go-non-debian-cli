## Blindfold go non-Debian client

Download the content of the folder

Download Anaconda (https://www.anaconda.com/)

Create and activate the conda environment
- $ conda env create --file environment.yaml
- $ conda activate blindfold-go-cli

Download FLAC
- Go to flac download page (https://xiph.org/flac/download.html)
- Choose OS (Windows, in your case)
- Download win.zip version (latest), probably at the end of the page. I downloaded this one (1.3.4-win.zip)
- Move to the download directory and extract it (You can simple use Extract Here)
- Move to win64 or win32 according to your system architecture
- Copy flac.exe and libFLAC.dll and paste them inside C:\Windows\System32

Try running your code.
- $ python cli.py

If it executes successfully, no need to do last step. If not, perform the following step too :

Open terminal in Administrator mode and execute the comments below :
- $ cd "C:\Windows\System32"
- $ ren "flac.exe" "flac"

Run your code again.
- $ python cli.py

