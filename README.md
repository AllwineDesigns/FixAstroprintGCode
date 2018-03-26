Hacky Astrobox Service to fix GCode for the Printrbot Simple Pro
================================================================

Info about the problem:

https://forum.astroprint.com/t/solved-having-trouble-with-a-printrbot-simple-pro/3168/3

To get the Printrbot Simple Pro to work with Astroprint, you need to follow
the instructions for updating the firmware so you can print over USB [here](https://printrbot.zendesk.com/hc/en-us/articles/115000151583-Printing-via-USB-on-Cura-2-with-Your-Printrbot-Simple-Pro?mobile_site=true).

Rather than setting up Cura 2, you'll set up an Astroprint printer with the
same almost all the same settings. You need to make a couple changes to the Start Commands. 
Change the 0.0 to the calibration setting on your Printrbot Simple Pro and
change material_print_temperature to print_temperature.

```
M100.1 ({{g55z: 0.0}}) ;Z-probe offset
G21 ;metric values
G90 ;absolute positioning
M82 ;set extruder to absolute mode
M107 ;start with the fan off
G28 X0 Y0 ;home X/Y
G28 Z0 ;home Z
G92 E0 ;zero the extruded length
G29 ;initiate auto bed leveling sequence
G55 ;apply z-offset value
G1 Z15.0 F9000
M109 S{print_temperature}
G92 E0
G1 F200 E10
G92 E0
G1 F9000
M117 Printing...
```

Astroprint is currently using Cura 15.04.6, whereas the Printrbot Simple Pro
needs Cura 2 (a newer version). As far as I can tell, though, the only thing
the older version of Cura doesn't know how to deal with is the {{g55z: 0.0}}.
The extra set of curly braces are replaced with question marks in the older version.
Manually removing the question marks is enough to get the gcode working. Instead
of manually doing it, the following service monitors the /AstroBoxFiles/uploads folder
for gcode files with an M100 line with questions marks on it and removes the question
marks.

To set up the service, sign into the Astrobox (you'll need an attached keyboard
and monitor as ssh isn't set up by default).

```
git clone https://github.com/AllwineDesigns/FixAstroprintGCode.git
sudo systemctl enable /home/pi/FixAstroprintGCode/fix_gcode.service
sudo systemctl start fix_gcode.service
```
