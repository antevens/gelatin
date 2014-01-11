#!/bin/bash

mkdir Gelatin.iconset
sips -z 16 16     World_Flag_Design_Universe.png --out Gelatin.iconset/icon_16x16.png
sips -z 32 32     World_Flag_Design_Universe.png --out Gelatin.iconset/icon_16x16@2x.png
sips -z 32 32     World_Flag_Design_Universe.png --out Gelatin.iconset/icon_32x32.png
sips -z 64 64     World_Flag_Design_Universe.png --out Gelatin.iconset/icon_32x32@2x.png
sips -z 128 128   World_Flag_Design_Universe.png --out Gelatin.iconset/icon_128x128.png
sips -z 256 256   World_Flag_Design_Universe.png --out Gelatin.iconset/icon_128x128@2x.png
sips -z 256 256   World_Flag_Design_Universe.png --out Gelatin.iconset/icon_256x256.png
sips -z 512 512   World_Flag_Design_Universe.png --out Gelatin.iconset/icon_256x256@2x.png
sips -z 512 512   World_Flag_Design_Universe.png --out Gelatin.iconset/icon_512x512.png
cp World_Flag_Design_Universe.png Gelatin.iconset/icon_512x512@2x.png

iconutil -c icns Gelatin.iconset
