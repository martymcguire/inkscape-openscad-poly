OpenSCAD Polygon Output for Inkscape
====================================

Notice
------

**This extension is no longer supported or maintained. The last tested version of Inkscape is 0.48.5.**

**Please feel free to fork and improve this extension for your own needs!**

This is an Inkscape extension that allows you to save your Inkscape drawings as
OpenSCAD (.scad) files containing modules with 2D polygons suitable for
extruding into 3D shapes.

Website: [http://github.com/martymcguire/inkscape-openscad-poly](http://github.com/martymcguire/inkscape-openscad-poly)

Contributors
============
* [Marty McGuire](http://github.com/martymcguire)
* [Benedict Endemann](https://github.com/baxerus)

Credits
=======

* This is a port of my [MakerBot Unicorn G-Code Output extension](http://github.com/martymcguire/inkscape-unicorn).
* [Inkscape](http://www.inkscape.org/) is an awesome open source vector graphics app.
* [OpenSCAD](http://www.openscad.org/) is an awesome open source language for creating 3D objects.
* [Scribbles](https://github.com/makerbot/Makerbot/tree/master/Unicorn/Scribbles%20Scripts) is the original DXF-to-Unicorn Python script.
* [The Egg-Bot Driver for Inkscape](http://code.google.com/p/eggbotcode/) provided inspiration and good examples for working with Inkscape's extensions API.

Install
=======

Copy the contents of `src/` to your Inkscape `extensions/` folder.

To find this folder you will need to check the instructions for your specific operating system and Inkscape installation type.

An incomplete list of possible locations by platform:

* OS X - `/Applications/Inkscape.app/Contents/Resources/extensions`
    * MacPorts (as required by [some newer versions of Inkscape](https://inkscape.org/release/inkscape-0.92.4/mac-os-x/macports/dl/)) has a different extensions folder. For example: `/opt/local/share/inkscape/extensions`.
* Linux - `/usr/share/inkscape/extensions`
* Windows - `C:\Program Files\Inkscape\share\extensions`

Usage
=====

* Size and locate your image appropriately:
	* Setting units to **mm** in Inkscape makes it easy to size your drawing.
	* The extension will automatically attempt to center everything.
* Convert all text to paths:
	* Select all text objects.
	* Choose **Path | Object to Path**.
* Save as OpenSCAD:
	* **File | Save a Copy**.
	* Select **OpenSCAD Polygons (\*.scad)**.
	* Save your file.

Use in OpenSCAD
===============

You'll find each path from your Inkscape file appears as a `module` in the
resulting OpenSCAD file.

The resulting OpenSCAD also contains a list of every generated module at the beginning. This allows easy control of the generated polygons by simply previewing in OpenSCAD (with F5 key) and can be easily disabled by commenting out or deleting the lines. If the paths in the SVG file use simple basic colors (no color gradient) this color is also transformed into an OpenSCAD color() statement and added before the module. Be aware that unfortunately OpenSCAD uses color only in preview mode (F5) not in render mode (F6).

For example:

	// my_drawing.scad
	module badge_face() {
	  polygon(points=
		[[-16.704628355490897, -20.69348168358303], [-13.479257330090903, -35.207652708983034], [-2.1904573300909078, -23.918852708983053], [17.161771644509102, -71.493081683583029], [-11.866570406290904, -40.045710658183026], [-13.479257330090903, -63.429652708983014], [-36.056857330090907, -56.172565785182996], [-30.412457330090902, -2.9539396327830048], [-0.57777040629089527, -1.3412527089830064], [16.355429593709104, -20.693481683583002], [38.126687542909096, -57.785252708983023]]
		, paths=
		[[0, 1, 2, 0], [3, 4, 5, 6, 7, 8, 9, 10, 3]]
		);}

You can include this file in your OpenSCAD program and use [OpenSCAD's 2D-to-3D extrusion methods](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#2D_to_3D_Extrusion), calling these modules to get the 2D data!

	// my_object.scad
	include <a_badge.scad>;

	linear_extrude(height=20)
	  badge_face();

TODOs
=====

* Use square and circle where applicable for simplicity?
* Combine layer contents into single modules?
* Parameterize smoothness for curve approximation (dirty workaround: Scale up in inkscape and down in OpenSCAD).
* Include example files/templates.

Special attribution notes
=========================
* File: test_svgs/3-Pointer_Altimeter.svg from [Wikimedia Commons](https://en.wikipedia.org/wiki/File:3-Pointer_Altimeter.svg) under _public domain_
