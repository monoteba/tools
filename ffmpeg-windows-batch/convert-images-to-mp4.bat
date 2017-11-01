@echo off

set format=.mp4
set lib=-c:v libx264

echo Convert to MP4 (H.264) 1920x1080
echo.


:: add current directory to PATH so we can run ffmpeg from here
cd ffmpeg\bin
set PATH=%PATH%;%CD%


:: get input folder
echo Drag folder with images into this window and press enter...
set /p input=
set input=%input:"=%\


:: get output file name
echo.
set /p output= Enter output file name: 


:: go to directory with images, and loop through all
cd %input%

if exist __ffmpeg_job.txt del __ffmpeg_job.txt

for %%a in (*.png) do (
	echo file '%input%%%a' >> __ffmpeg_job.txt
)


:: convert!
set input_args=-r 12 -f concat -safe 0 -i __ffmpeg_job.txt
set output_args=-r 24 -c copy -crf 30 -b:v 0
set scale_args=-vf scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2

ffmpeg.exe %input_args% %output_args% %lib% %scale_args% "%output%%format%"


:: delete the job text file and
del __ffmpeg_job.txt

echo.
echo Done! Saved file to:
echo %input%%output%%format%
echo.
echo Press enter to close this window...
@pause >nul
