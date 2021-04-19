#! /bin/bash

for f in `find . -type f -name *.png`; do
	w=$(magick identify -format "%w" "${f}"); 
	h=$(magick identify -format "%h" "${f}");

	let width=${w}/4*4;
	let height=${h}/4*4;

	if [ $w -ne $width ]; then
		let width=${width}+4
	fi

	if [ $h -ne $height ]; then
		let height=${height}+4
	fi

	if [ $w -ne $width ] || [ $h -ne $height ]; then
		echo "Resizing: ${f}";
		magick convert "${f}" -background none -gravity center -extent "${width}x${height}" "${f}";
	fi
done