import unittest
import os
import numpy as np

import geosoft
import geosoft.gxpy.gx as gx
import geosoft.gxpy.utility as gxu
import geosoft.gxpy.system as gsys
import geosoft.gxpy.map as gxmap
import geosoft.gxpy.geometry as gxgm
import geosoft.gxpy.view as gxv
import geosoft.gxapi as gxapi
import geosoft.gxpy.viewer as gxvwr


def rect_line(view, size=100):
    view.xy_rectangle(gxgm.Point((0, 0)), gxgm.Point((1, 1)) * size, pen={'line_thick': 1})
    p1 = gxgm.Point((0.1, 0.1)) * size
    p2 = gxgm.Point((0.9, 0.9)) * size
    poff = gxgm.Point((0.15, 0.05)) * size
    view.pen = {'fill_color': gxapi.C_LT_GREEN}
    view.xy_rectangle(p1, p2)
    view.pen = {'line_style': (2, 2.0)}
    view.xy_line(p1 + poff, p2 - poff)


def draw_stuff(view, size = 1.0):
    plinelist = [[110, 5],
                 [120, 20],
                 [130, 15],
                 [150, 50],
                 [160, 70],
                 [175, 35],
                 [190, 65],
                 [220, 50],
                 [235, 18.5]]

    pp = gxgm.PPoint.from_list(plinelist) * size
    view.pen = {'line_style': (2, 2.0)}
    view.xy_poly_line(pp)
    view.pen = {'line_style': (4, 2.0), 'line_smooth': gxv.SMOOTH_AKIMA}
    view.xy_poly_line(pp)

    ppp = np.array(plinelist)
    pp = gxgm.PPoint(ppp[3:, :]) * size
    view.pen = {'line_style': (5, 5.0),
                  'line_smooth': gxv.SMOOTH_CUBIC,
                  'line_color': gxapi.C_RED,
                  'line_thick': 0.25,
                  'fill_color': gxapi.C_LT_BLUE}
    view.xy_poly_line(pp, close=True)

    view.pen = {'fill_color': gxapi.C_LT_GREEN}
    p1 = gxgm.Point((100, 0, 0)) * size
    p2 = gxgm.Point((100, 0, 0)) * size
    pp = (pp - p1) / 2 + p2
    view.xy_poly_line(pp, close=True)
    pp += gxgm.Point((0, 25, 0)) * size
    view.pen = {'fill_color': gxapi.C_LT_RED}
    view.xy_poly_line(pp, close=True)


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gx = gx.GXpy(log=print, parent_window=-1)
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    
    @classmethod
    def start(cls,test):
        cls.gx.log("\n*** {} *** - {}".format(test, geosoft.__version__))

    def test_version(self):
        self.start(gsys.func_name())
        self.assertEqual(gxmap.__version__, geosoft.__version__)

    def test_create(self):
        self.start(gsys.func_name())

        with gxv.GXview():
            pass

        with gxv.GXview() as vw:
            self.assertEqual(vw.viewname, "_default_view")

        with gxv.GXview("test") as vw:
            self.assertEqual(vw.viewname, "test")

        test_map = os.path.join(self.gx.temp_folder(),"test_map")
        gmap = gxmap.GXmap.new(test_map)
        mapname = gmap.mapfilename
        with gxv.GXview("test", gmap) as view:
            self.assertEqual(view.viewname, "test")
            self.assertEqual(view.mapfilename, mapname)

            def_pen = view.pen
            pn = {"line_thick": 99, "pat_number": 88}
            view.push_pen()
            view.pen = pn
            new_pen = view.pen
            self.assertEqual(new_pen["line_thick"], 99)
            self.assertEqual(new_pen["pat_number"], 88)

            view.pop_pen()
            pen = view.pen
            self.assertEqual(pen, def_pen)

            view.push_pen(pn)
            view.pen = pn
            new_pen = view.pen
            self.assertEqual(new_pen["line_thick"], 99)
            self.assertEqual(new_pen["pat_number"], 88)

            view.pop_pen()
            pen = view.pen
            self.assertEqual(pen, def_pen)


    def test_view(self):
        self.start(gsys.func_name())

        testmap = os.path.join(self.gx.temp_folder(), "test")
        with gxmap.GXmap.new(testmap, overwrite=True) as gmap:
            mapfile = gmap.mapfilename
            with gxv.GXview("rectangle_test", gmap) as view:
                rect_line(view)
            with gxv.GXview("poly", gmap) as view:
                draw_stuff(view)

        gxvwr.map(mapfile)
        self.assertEqual(gxmap.crc_map(mapfile), 1477469463)
        gxmap.delete_files(mapfile)

    def test_3D(self):
        self.start(gsys.func_name())

        testmap = os.path.join(self.gx.temp_folder(), "test")
        testmap = "test"
        with gxmap.GXmap.new(testmap, overwrite=True) as gmap:
            mapfile = gmap.mapfilename
            with gxv.GXview("base", gmap) as view:
                view.xy_rectangle(gxgm.Point((0,0)), gxgm.Point((100,100)))
            with gxv.GXview3d(viewname='v3d_test', locate=(0,0,100,100), area=(0,0,10,10),
                              gmap=gmap, hcs="wgs 84 / UTM zone 15S") as view:
                rect_line(view)
                draw_stuff(view)
                view.box_3d(gxgm.Box(gxgm.Point((0,0,10)), gxgm.Point((120,100,50))))

        gxvwr.map(mapfile)
        gxvwr.v3d(mapfile)

    def test_cs(self):
        self.start(gsys.func_name())

        testmap = os.path.join(self.gx.temp_folder(), "test")
        with gxmap.GXmap.new(testmap, overwrite=True) as gmap:
            with gxv.GXview("rectangle_test", gmap=gmap, hcs="wgs 84") as view:
                cs = view.cs
                self.assertTrue("WGS 84" in cs[0])
                self.assertEqual(cs[1], None)
            with gxv.GXview("vcs", gmap=gmap, hcs="wgs 84", vcs="special") as view:
                cs = view.cs
                self.assertTrue("WGS 84" in cs[0])
                self.assertEqual(cs[1], "special")

if __name__ == '__main__':

    unittest.main()
