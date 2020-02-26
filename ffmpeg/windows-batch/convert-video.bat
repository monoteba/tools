@echo off

cd
set start_path=%CD%

:start
cd %start_path%
cls
echo CONVERT VIDEO
echo Resolution: Original
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
)

:: ask for video format
:prompt
echo.
echo Enter number of video format to use:
echo 1: MP4 (H.264), AAC 256k audio
echo 2: WebM (VP9), OPUS 256k audio
echo 3: Prores HQ (422), PCM 16-bit audio
echo 4: Prores HQ (4444), PCM 16-bit audio
echo.

set format=
set lib=
set audio=

set /p format_option= Enter number:

:: mp4 h.264
if "%format_option%"=="1" (
	set format=.mp4
	set lib=-c:v libx264 -crf 18 -pix_fmt yuv420p
	set audio=-c:a aac -b:a 256k
)

:: webm vp9
if "%format_option%"=="2" (
	set format=.webm
	set lib=-c:v libvpx-vp9 -b:v 0 -crf 15
	set audio=-c:a libopus -b:a 256k
)

:: prores 422
if "%format_option%"=="3" (
	set format=.mov
	set lib=-c:v prores_ks -profile:v 3 -qscale:v 5 -vendor ap10 -pix_fmt yuv422p10le
	set audio=-c:a pcm_s16le
)

:: prores 4444
if "%format_option%"=="4" (
	set format=.mov
	set lib=-c:v prores_ks -profile:v 4444 -qscale:v 5 -vendor ap10 -pix_fmt yuva444p10le
	set audio=-c:a pcm_s16le
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
:: set scale_args=-vf scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2
set scale_args=

ffmpeg.exe -loglevel info %input_args% %lib% %scale_args% %audio% "%input_path:"=%%output%%format%"

echo.
echo Done! Saved file to:
echo %input_path:"=%%output%%format%
echo.
echo Press enter to continue...
@pause >nul
cls
goto start
