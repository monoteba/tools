@echo off

cd
set start_path=%CD%

:start
cd %start_path%
cls
echo CONVERT VIDEO
echo Resolution: 1920x1080
echo Frame-rate: Original
echo.

:: add ffmpeg to path
cd ffmpeg\bin
set PATH=%PATH%;%CD%

:: ask for input folder
echo Drag video file into this window and press enter...
set /p input=
set input_path=

:: goto to folder of video
for %%a in (%input%) do (
	set input_path="%%~dpa"
	cd %input_path%
)

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

:: clear screen before converting
cls
echo Converting...
echo.

:: convert!
set input_args=-i %input%
set output_args=-crf 30 -c copy -b:v 0
set scale_args=-vf scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2

ffmpeg.exe -loglevel warning %input_args% %output_args% %lib% %scale_args% "%output%%format%"

echo.
echo Done! Saved file to:
echo %input_path:"=%%output%%format%
echo.
echo Press enter to continue...
@pause >nul
cls
goto start