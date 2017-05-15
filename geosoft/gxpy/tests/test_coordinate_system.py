import unittest
import numpy as np
import json

import geosoft.gxapi as gxapi
import geosoft.gxpy.gx as gx
import geosoft.gxpy.system as gsys
import geosoft.gxpy.coordinate_system as gxcs
import geosoft

from geosoft.gxpy.tests import GXPYTest


class Test(GXPYTest):

    def test_any(self):
        self.start()

        # name
        with gxcs.Coordinate_system( 'DHDN / Okarito 2000') as cs:
            gxfs = cs.gxf
            self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
            self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
            self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
            self.assertEqual(gxfs[3],'m,1')
            self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')
            self.assertEqual(cs.cs_name(),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), '')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_DATUM),'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_PROJECTION),'Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_ORIENTATION),'0,0,0,0,0,0')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT),'m')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT_FULL),'metre')

        # GXF strings
        with gxcs.Coordinate_system(['','DHDN','Okarito 2000','','']) as cs:
            gxfs = cs.gxf
            self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
            self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
            self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
            self.assertEqual(gxfs[3],'m,1')
            self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')

        # dictionary, json
        with gxcs.Coordinate_system('DHDN / Okarito 2000') as cs:
            dct = cs.coordinate_dict()
            with gxcs.Coordinate_system(dct) as cs:
                gxfs = cs.gxf
                self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
                self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
                self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
                self.assertEqual(gxfs[3],'m,1')
                self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')

                csd = cs.coordinate_dict()
                self.assertEqual(csd['name'],'DHDN / Okarito 2000')
                self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
                self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
                self.assertEqual(gxfs[3],'m,1')
                self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')

                js = json.dumps(dct)
                with gxcs.Coordinate_system(js) as cs:
                    gxfs = cs.gxf
                    self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
                    self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
                    self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
                    self.assertEqual(gxfs[3],'m,1')
                    self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')

        # name with a separate vcs
        with gxcs.Coordinate_system('DHDN / Okarito 2000') as cs:
            cs.vcs = 'geoid'
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), str(cs))
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), 'geoid')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN / Okarito 2000 [geoid]')

        # name with embedded vcs
        with gxcs.Coordinate_system('DHDN / Okarito 2000 [geoid]') as cs:
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), str(cs))
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), 'geoid')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN / Okarito 2000 [geoid]')

        ipj = gxapi.GXIPJ.create()
        ipj.set_gxf('', 'DHDN', 'Okarito 2000', '', '')
        with gxcs.Coordinate_system(ipj) as cs:
            gxfs = cs.gxf
            self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
            self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
            self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
            self.assertEqual(gxfs[3],'m,1')
            self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')
            self.assertEqual(cs.cs_name(),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), '')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_DATUM),'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_PROJECTION),'Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_ORIENTATION),'0,0,0,0,0,0')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT),'m')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT_FULL),'metre')

        with gxcs.Coordinate_system(gxcs.Coordinate_system(ipj)) as cs:
            self.assertEqual(cs.vcs, '')
            gxfs = cs.gxf
            self.assertEqual(gxfs[0],'DHDN / Okarito 2000')
            self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
            self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
            self.assertEqual(gxfs[3],'m,1')
            self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')
            self.assertEqual(cs.cs_name(),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), '')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_DATUM),'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_PROJECTION),'Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_ORIENTATION),'0,0,0,0,0,0')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT),'m')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT_FULL),'metre')

    def test_name_cs(self):
        self.start()

        hcs, orient, vcs = gxcs.hcs_orient_vcs_from_name("DHDN / Okarito 2000 [geoid]")
        self.assertEqual(hcs, "DHDN / Okarito 2000")
        self.assertEqual(orient, "")
        self.assertEqual(vcs, "geoid")
        self.assertEqual(gxcs.name_from_hcs_orient_vcs(hcs, orient, vcs), "DHDN / Okarito 2000 [geoid]")

        hcs, orient, vcs = gxcs.hcs_orient_vcs_from_name("DHDN / Okarito 2000    <0,0,0,0,0,0>  [geoid]     ")
        self.assertEqual(hcs, "DHDN / Okarito 2000")
        self.assertEqual(orient, "0,0,0,0,0,0")
        self.assertEqual(vcs, "geoid")
        self.assertEqual(gxcs.name_from_hcs_orient_vcs(hcs, orient, vcs), "DHDN / Okarito 2000 <0,0,0,0,0,0> [geoid]")

        hcs, orient, vcs = gxcs.hcs_orient_vcs_from_name("DHDN / Okarito 2000 <0,0,0,0,0,0>")
        self.assertEqual(hcs, "DHDN / Okarito 2000")
        self.assertEqual(orient, "0,0,0,0,0,0")
        self.assertEqual(vcs, "")
        self.assertEqual(gxcs.name_from_hcs_orient_vcs(hcs, orient, vcs), "DHDN / Okarito 2000 <0,0,0,0,0,0>")

        hcs, orient, vcs = gxcs.hcs_orient_vcs_from_name("DHDN / Okarito 2000")
        self.assertEqual(hcs, "DHDN / Okarito 2000")
        self.assertEqual(orient, "")
        self.assertEqual(vcs, "")
        self.assertEqual(gxcs.name_from_hcs_orient_vcs(hcs, orient, vcs), "DHDN / Okarito 2000")

        with gxcs.Coordinate_system( 'DHDN / Okarito 2000 [geodetic]') as cs:
            gxfs = cs.gxf
            self.assertEqual(gxfs[0],'DHDN / Okarito 2000 [geodetic]')
            self.assertEqual(gxfs[1],'DHDN,6377397.155,0.0816968312225275,0')
            self.assertEqual(gxfs[2],'"Transverse Mercator",-43.11,170.260833333333,1,400000,800000')
            self.assertEqual(gxfs[3],'m,1')
            self.assertEqual(gxfs[4],'"DHDN to WGS 84 (1)",582,105,414,1.04,0.35,-3.08,8.29999999996112')
            self.assertEqual(cs.cs_name(),'DHDN / Okarito 2000 [geodetic]')
            self.assertEqual(cs.cs_name(what=gxcs.NAME),'DHDN / Okarito 2000 [geodetic]')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS),'DHDN / Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), 'geodetic')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_DATUM),'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_PROJECTION),'Okarito 2000')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_ORIENTATION),'0,0,0,0,0,0')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT),'m')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_UNIT_FULL),'metre')

        with gxcs.Coordinate_system('DHDN [geoid]') as cs:
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), cs.name)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS), cs.hcs)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), cs.vcs)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS), 'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), 'geoid')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN [geoid]')

        with gxcs.Coordinate_system('DHDN [geodetic]') as cs:
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), cs.name)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS), cs.hcs)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), cs.vcs)
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS), 'DHDN')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_VCS), 'geodetic')
            self.assertEqual(cs.cs_name(what=gxcs.NAME_HCS_VCS), 'DHDN [geodetic]')

    def test_vcs(self):
        self.start()

        self.assertEqual(gxcs.Coordinate_system("nad83 / UTM zone 15N [NAVD92]").name, 'NAD83 / UTM zone 15N [NAVD92]')
        self.assertEqual(gxcs.Coordinate_system("nad83 [NAVD92]").name, 'NAD83 [NAVD92]')
        self.assertFalse(gxcs.Coordinate_system("nad83 [NAVD92]").same_as(gxcs.Coordinate_system("NAD83 [geodetic]")))
        self.assertFalse(gxcs.Coordinate_system("nad83 [geoid]").same_vcs(gxcs.Coordinate_system("NAD27 [NAVD92]")))

    def test_pj(self):
        self.start()

        with gxcs.Coordinate_system('DHDN / Okarito 2000') as cs:
            with gxcs.Coordinate_system('DHDN') as csll:
                with gxcs.Coordinate_translate(cs, csll) as pj:

                    lon, lat = pj.convert((500000, 6500000))
                    self.assertAlmostEqual(lon, 171.168823147)
                    self.assertAlmostEqual(lat, 8.36948254242)

                    lon, lat, z = pj.convert((500000, 6500000, 50))
                    self.assertAlmostEqual(lon, 171.168823147)
                    self.assertAlmostEqual(lat, 8.36948254242)
                    self.assertAlmostEqual(z, 50)

                    ll = pj.convert([[500000, 6500000], [505000, 6510000]])
                    self.assertAlmostEqual(ll[0][0], 171.168823147)
                    self.assertAlmostEqual(ll[0][1], 8.36948254242)
                    self.assertAlmostEqual(ll[1][0], 171.214439577)
                    self.assertAlmostEqual(ll[1][1], 8.45978927383)

                    ll = pj.convert(np.array([[500000, 6500000], [505000, 6510000]]))
                    self.assertTrue(type(ll) is np.ndarray)
                    self.assertAlmostEqual(ll[0][0], 171.168823147)
                    self.assertAlmostEqual(ll[0][1], 8.36948254242)
                    self.assertAlmostEqual(ll[1][0], 171.214439577)
                    self.assertAlmostEqual(ll[1][1], 8.45978927383)

    def test_localgrid(self):
        self.start()

        self.assertRaises(gxcs.CSException, gxcs.Coordinate_system, {'type': 'local'})

        csdict = {'type': 'local', 'lon_lat': (-96,43)}
        csd = gxcs.Coordinate_system(csdict)
        self.assertEqual(csd.name, 'WGS 84 / *Local(43,-96,0,0)')

        with gxcs.Coordinate_translate(csd, gxcs.Coordinate_system('WGS 84')) as pj:
            lon, lat, z = pj.convert((0, 0, 0))
            self.assertAlmostEqual(lat, 43)
            self.assertAlmostEqual(lon, -96)
            self.assertAlmostEqual(z, 0)

        csdict['azimuth'] = 25
        csd = gxcs.Coordinate_system(csdict)
        self.assertEqual(csd.name, 'WGS 84 / *Local(43,-96,0,0) <0,0,0,0,0,25>')
        self.assertEqual(csd.gxf[2], '"Oblique Stereographic",43,-96,0.9996,0,0')

        with gxcs.Coordinate_translate(gxcs.Coordinate_system('WGS 84'), csd) as pj:
            x, y, z = pj.convert((-96, 43, 0))
            self.assertAlmostEqual(x, 0)
            self.assertAlmostEqual(y, 0)
            self.assertAlmostEqual(z, 0)
            x, y, z = pj.convert((-95, 43, 0))
            self.assertAlmostEqual(x, 73665.899715)
            self.assertAlmostEqual(y, 34886.2319719)
            self.assertAlmostEqual(z, 0)

        csdict['origin'] = (1800, 500)
        csd = gxcs.Coordinate_system(csdict)
        self.assertEqual(csd.name, 'WGS 84 / *Local(43,-96,1800,500) <0,0,0,0,0,25>')
        self.assertEqual(csd.gxf[2], '"Oblique Stereographic",43,-96,0.9996,1842.66314753632,-307.558977614934')

        csdict['elevation'] = 800.5
        csdict['vcs'] = 'geoid'
        csd = gxcs.Coordinate_system(csdict)
        self.assertEqual(csd.name, 'WGS 84 / *Local(43,-96,1800,500) <0,0,800.5,0,0,25>')
        self.assertEqual(csd.gxf[2], '"Oblique Stereographic",43,-96,0.9996,1842.66314753632,-307.558977614934')
        with gxcs.Coordinate_translate(gxcs.Coordinate_system('WGS 84'), csd) as pj:
            x, y = pj.convert((-96, 43))
            self.assertAlmostEqual(x, 1800)
            self.assertAlmostEqual(y, 500)
        with gxcs.Coordinate_translate(csd, gxcs.Coordinate_system('WGS 84')) as pj:
            lon, lat, z = pj.convert((1800, 500, 0))
            self.assertAlmostEqual(lat, 43)
            self.assertAlmostEqual(lon, -96)
            self.assertAlmostEqual(z, 800.5)

    def test_oriented(self):
        self.start()

        with gxcs.Coordinate_system({'type': 'local', 'lon_lat': (-96,43), 'azimuth':25}) as cs:

            xyzo = (10, 0, 0)
            xyz = cs.xyz_from_oriented(xyzo)
            self.assertEqual(xyz, (9.063077870366499, -4.2261826174069945, 0.0))

            xyz = (9.063077870366499, -4.2261826174069945, 0.0)
            xyz = cs.oriented_from_xyz(xyz)
            self.assertAlmostEqual(xyz[0], xyzo[0])
            self.assertAlmostEqual(xyz[1], xyzo[1])
            self.assertAlmostEqual(xyz[2], xyzo[2])

            xyzo = ((10, 0, 0), (0, 10,5))
            xyz = cs.xyz_from_oriented(xyzo)
            self.assertEqual(tuple(xyz[0]), (9.063077870366499, -4.2261826174069945, 0.0))
            self.assertEqual(tuple(xyz[1]), (4.2261826174069945, 9.0630778703664987, 5.0))

            xyz = ((9.063077870366499, -4.2261826174069945, 0.0), (4.2261826174069945, 9.0630778703664987, 5.0))
            xyz = cs.oriented_from_xyz(xyz)
            self.assertAlmostEqual(xyz[0][0], xyzo[0][0])
            self.assertAlmostEqual(xyz[0][1], xyzo[0][1])
            self.assertAlmostEqual(xyz[0][2], xyzo[0][2])

            xyzo = ((10, 0), (0, 10), (0, 5))
            xyz = cs.xyz_from_oriented(xyzo, column_ordered=True)
            self.assertEqual(tuple(xyz[0]), (9.063077870366499, 4.2261826174069945))
            self.assertEqual(tuple(xyz[1]), (-4.2261826174069945, 9.063077870366499))
            self.assertEqual(tuple(xyz[2]), (0.0, 5.0))

    def test_parameters(self):
        self.start()

        self.assertTrue(gxcs.parameter_exists(gxcs.PARM_DATUM, 'NAD83'))
        self.assertTrue(gxcs.parameter_exists(gxcs.PARM_PROJECTION, 'UTM zone 15N'))
        self.assertTrue(gxcs.parameter_exists(gxcs.PARM_UNITS, 'ftUS'))
        self.assertTrue(gxcs.parameter_exists(gxcs.PARM_LOCAL_DATUM, gxcs.name_list(gxcs.LIST_LOCALDATUMNAME)[5]))
        self.assertFalse(gxcs.parameter_exists(gxcs.PARM_UNITS, 'hoofs'))

        params = gxcs.parameters(gxcs.PARM_DATUM, 'WGS 84')
        self.assertTrue('ELLIPSOID' in params)

        params = gxcs.parameters(gxcs.PARM_PROJECTION, 'UTM zone 15N')
        self.assertEqual(float(params['P5']), 0.9996)

###############################################################################################

if __name__ == '__main__':

    unittest.main()
