Laser Safety Calculator.

The lasersafety.py script contained within the same folder as this file runs a programme that will output safety information based on the laser parameters
that the user inputs.

To start, simply run the programme. A prompt will appear asking the user to decide between the continuous wave mode (press 'c'), the repetitive pulse mode
(press 'r'), or for extra information (press 'h'). Based on the mode chosen, different variable inputs will pop up.


Variables for both modes:

Wavelength - This is the wavelength of the laser. Enter this value in nanometers. The programme can handle values ranging between 180 nm and 1,000,000 nm. 
		Any value outside this range will result in an error message. The wavelength can be input using integers, decimals or via scientific notation 
		(i.e., 1e6 to represent 1,000,000).

Exposure time - This is the expected duration of the exposure to the laser radiation. Enter this value in seconds. Again, very small numbers, such as 1 ns can be 
		input using scientific notation (1e-9). If this value is unknown to the user then it can be left blank. The programme will use a default exposure 
		time based on the wavelength of the laser.

Diameter of limiting aperture - This is the minimum diameter that the laser is expected to pass through. Enter this value in meters. If the value is unknown, it can
				be left blank. The default value is obtained using the wavelength and exposure time of the laser. 

Beam divergence - This is how much the beam spreads out from the source. Enter this value in radians. If the value is unknown, it can be left blank.


Variables for continous wave:

Radiant power - This is the power that the laser is equipped with. Enter this value in Watts. This value cannot be left blank, or the programme will pop up with
		an error. 

Spectral reflectance - This is the ratio of the energy reflected by a surface to the energy incident on a surface. This value is unitless and can be left blank.

Reflectance - This asks the user to choose between diffuse (press 'd') or specular (press 's') reflectance. If unknown, the programme will choose specular reflectance
		by default, as this will result in larger NHZ values. 


Variables for repetitive pulse:

Pulse width - This is the duration of one pulse of the laser. Enter this value in seconds. It cannot be left blank.

Energy per pulse - This is the energy that each pulse of the laser contains. Enter this value in Joules. It cannot be left blank.

Frequency - This is how often the laser pulses. Enter this value in Hertz. It cannot be left blank. 


Once all the parameters are input, the programme will carry out the calculations and output safety information, such as the minimum optical density required of a lens
to protect the eye from laser radiation within the expected exposure time. 