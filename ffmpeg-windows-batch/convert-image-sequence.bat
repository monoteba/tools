@echo off

cd
set start_path=%CD%

:start
cd %start_path%
cls
echo CONVERT IMAGES TO VIDEO
echo Resolution: 1920x1080
echo Frame-rate: 24 (input is 12)
echo.

:: add ffmpeg to path
cd ffmpeg\bin
set PATH=%PATH%;%CD%

:: ask for input folder
echo Drag folder with images (.png OR .jpg) into this window and press enter...
set /p input=
set input=%input:"=%\
cd %input%

:: verify folder does NOT contain more than 1 image type
set /a format_count=0
if exist "%input%*.png" (set /a format_count+=1)
if exist "%input%*.jpg" (set /a format_count+=1)

if %format_count% gtr 1 (goto error)

:: ask for video format
:prompt
echo.
echo Enter number of video format to use:
echo 1: MP4/H.264
echo 2: WebM
echo.

set format=
set lib=

set /p format_option= Enter number: 

if %format_option%==1 (
	set format=.mp4
	set lib=-c:v libx264
)

if %format_option%==2 (
	set format=.webm
	set lib=-c:v libvpx-vp9
)

if not defined format (
	echo.
	echo Try again...
	echo.
	goto prompt
)

:: ask for output file name
echo.
set /p output= Enter output file name (without %format%): 

:: create file with images to convert
if exist __ffmpeg_job.txt del __ffmpeg_job.txt

for %%a in (*.png *.jpg) do (
	:: ~dpnxa = drive, path, name, ext of file
	echo file '%%~dpnxa' >> __ffmpeg_job.txt
)

:: clear screen before converting
cls
echo Converting...
echo.

:: convert!
set input_args=-r 12 -f concat -safe 0 -i __ffmpeg_job.txt
set output_args=-r 24 -crf 30 -c copy -b:v 0
set scale_args=-vf scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2

ffmpeg.exe -loglevel warning %input_args% %output_args% %lib% %scale_args% "%output%%format%"

:: delete the job text file and
del __ffmpeg_job.txt

echo.
echo Done! Saved file to:
echo %input%%output%%format%
echo.
echo Press enter to continue...
@pause >nul
cls
goto start

:error
cls
echo [91mThe folder contained both .png and .jpg images. 
echo The folder must only contain images in the same format^![0m
echo.
echo Press enter to continue...
@pause >nul
cls
goto start