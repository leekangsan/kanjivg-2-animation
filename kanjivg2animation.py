#Description:
#              This script will convert kanjiVG's svg files into animations that reveal the stroke
#              order of different kanji. All animations are done in accordance to the SVG animation
#              standard, which is not supported by Internet Explorer. JavaScript is used only
#              to provide the pause, play and reset features.
#
#Prerequisites:
#              kanjiVG :  https://github.com/KanjiVG/kanjivg (CC BY-SA 3.0) [unpack in /kanji/ folder]
#              svg.path:  https://pypi.python.org/pypi/svg.path [place in /path/ subfolder]
#
#Usage:
#              If needed, edit the /kanji/ directory below with the proper path for the kanjiVG files,
#              then update the /converted/ directory to indicate where the converted files should be placed.
#              Please note that svg.path is very resource-intensive and very slow, so this script
#              could take an extremely long time to parse the thousand svg files.
#
#Similar projects:
#              https://github.com/mbilbille/dmak
#              https://github.com/Kimtaro/kanjivg2svg

import math
import os
import sys
sys.path.append('path')
import path

#A function that allows you to retrieve a string between two specified strings
def find_between(s, first, last):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

#Iterate through each svg file in the kanji directory.
for file in os.listdir("/kanji"):
    #Our source and target files and directories
    source_file = open("/kanji/" + file, 'r', encoding="utf8")
    target_file = open("/converted/" + file[:-4] + '-jlect.svg', 'w+', encoding="utf8")

	#The array that we will use to build the various parts comprising the svg
    svg_build_array = []

	#The array that will contain all values of 'd' (the path code) in the original svg file
    dpath = []

	#Retrieve the value of 'd' (the path code) in the original svg file
    for line in source_file:
        if "<path" in line and "d=\"" in line:
            dpath.append(find_between(line, " d=\"", "\"/>"))

    source_file.close()

	#Start building an array that contains the fragments of our svg
    svg_build_array.append("<svg id=\"kvg-" + file[:-4] + "\" class=\"kanjivg\" width=\"106\" height=\"126\" ")
	
    ##Thought: maybe make end animation last longer before repeat? Or maybe keep it permanent?
    
	#Begin defining the svg, its components and their styles
    svg_build_array.append("""xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" baseProfile="full"><defs><style type="text/css"><![CDATA[path.black{fill:none;stroke:black;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}path.grey{fill:none;stroke:#ddd;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}path.stroke{fill:none;stroke:black;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}rect{fill:none;stroke:#555;stroke-width:2;} text{font-size:16px;font-family:Segoe UI Symbol,Cambria Math,DejaVu Sans,Symbola,Quivira,STIX,Code2000;-webkit-touch-callout:none;cursor:pointer;-webkit-user-select:none;-khtml-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select: none;}text:hover{color:#777;}#reset{font-weight:bold;}]]></style><marker id="markerStart" markerWidth="8" markerHeight="8" style="overflow:visible;"><circle cx="0" cy="0" r="1.5" style="stroke:none;fill:red;fill-opacity:0.5;"/></marker><marker id="markerEnd" style="overflow:visible;"><circle cx="0" cy="0" r="0.8" style="stroke:none;fill:blue;fill-opacity:0.5;"><animate attributeName="opacity" from="1" to="0" dur="3s" repeatCount="indefinite" /></circle></marker></defs>""")

    svg_build_array.append('<rect x="4" y="4" width="100" height="100" />')

	#First we draw the grey kanji strokes in the background, without any animations
    for a in dpath:
        svg_build_array.append('<path d="' + a + '" class="grey" />')

	#The value of i represents 
    i = 0.0
	
	#Then we handle the black kanji strokes, which will be animated in the foreground
    for b in dpath:
        path_length = path.parse_path(b).length()
        stroke_length = 150
		
		#Change the stroke length if the path length exceeds our expectations
        if path_length > 150 and path_length < 200:
            stroke_length = 200
        elif path_length > 200  and path_length < 250:
            stroke_length = 250
        elif path_length > 250:
            stroke_length = 300
        
		#Begin handling the path
        svg_build_array.append('<path d="' + b + '" class="stroke" stroke-dasharray="' + str(stroke_length) + '">')
		
		#Hide the black stroke for a specified duration (dur)
        if i is not 0:
            svg_build_array.append('<set attributeName="opacity" to="0" dur="' + str(i) + 's" />')
		
		#Animate the black stroke after a specified duration (begin)
        svg_build_array.append('<animate attributeName="stroke-dashoffset" from="' + str(stroke_length) + '" to="0" dur="1.8s" begin="' + str(i) + 's" fill="freeze" />')
		
		#Finish handling the path
        svg_build_array.append('</path>')

        #Given the length of the current path, calculate the amount of time we should add to 'i'. The next path will animate after that time.
        if path_length < 20:
            i += 0.9
        elif path_length < 40:
            i += 1.0
        elif path_length < 45:
            i += 1.1
        elif path_length < 50:
            i += 1.2
        elif path_length < 55:
            i += 1.3
        elif path_length < 60:
            i += 1.4
        elif path_length < 70:
            i += 1.5
        elif path_length < 90:
            i += 1.7
        elif path_length < 100:
            i += 1.8
        elif path_length < 110:
            i += 1.9
        else:
            i += 2.0 #TODO: REPLACE THESE WITH FORMULA? User-changeable speed?

    #Add the Pause/Play and Reset buttons.
    svg_build_array.append('<text x="90" y="120" id="reset">⟳</text><text x="70" y="120" id="pause">◼</text>')
	
	#Minified JavaScript that handles the above buttons
    svg_build_array.append('<script type="text/javascript"><![CDATA[') #should this be text/javascript or text/ecmascript?
    svg_build_array.append('function RecurringTimer(e,t){var n,r,i=t;this.pause=function(){window.clearTimeout(n);i-=new Date-r};var s=function(){r=new Date;n=window.setTimeout(function(){i=t;s();e()},i)};this.clear=function(){window.clearTimeout(n);i=t;n=window.setTimeout(function(){i=t;s();e()},i)};this.resume=s;this.resume()}function invoketimer(){timer=new RecurringTimer(function(){svg.setCurrentTime(0)},' + str(float((i*1000) + 1000)) + ')}var svg=document.getElementById("kanjivg");var pause=document.getElementById("pause");var reset=document.getElementById("reset");var timer;invoketimer();reset.onclick=function(){svg.setCurrentTime(0);timer.clear();svg.unpauseAnimations();pause.innerHTML = "◼";};pause.onclick=function(){if(svg.animationsPaused()){svg.unpauseAnimations();timer.resume();pause.innerHTML="◼"}else{svg.pauseAnimations();timer.pause();pause.innerHTML="▶"}}')
    svg_build_array.append(']]></script>')

	#Finish handling the svg
    svg_build_array.append('</svg>')

	#Write the svg build array to a file
    for item in svg_build_array:
        target_file.write(item)
    
	#Close the file
    target_file.close()

#When the script is finished converting all files in the specified directory, it will print the following message to indicate it has finished.
print("Done.")
