$images = Get-ChildItem -Filter *.png -Recurse;
$count = $images.Count;
$idx = 0;

foreach ($img in $images)
{
    # stop if escape key is pressed (27)
    if ($Host.UI.RawUI.KeyAvailable -and (27 -eq $Host.UI.RawUI.ReadKey("IncludeKeyUp,NoEcho").VirtualKeyCode)) 
    {
        break;
    }

    $w = iex 'magick identify -format "%w" $($img.FullName)';
    $h = iex 'magick identify -format "%h" $($img.FullName)';

    $modify = 0;

    if (-NOT ($w % 4 -eq 0))
    {
        $w = ([math]::truncate($w / 4.0) + 1) * 4;
        $modify++;
    }

    if (-NOT ($h % 4 -eq 0))
    {
        $h = ([math]::truncate($h / 4.0) + 1) * 4;
        $modify++;
    } 

    $idx++;
    echo "Processing image $idx of $count";

    if (($modify -eq 0))
    {
        echo "Skip >> $($img.Name)";
        continue;
    }

    echo "Convert >> $($img.Name) ($w x $h px)";
    $cmd = 'magick convert $($img.FullName) -background none -gravity center -extent "$($w)x$($h)" $($img.FullName)';
    iex $cmd;
}