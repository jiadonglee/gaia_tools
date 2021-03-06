# Tests of gaia_tools.select.tgasSelect
import numpy
import gaia_tools.select

def test_effvol_complete():
    # Test that the effective volume == volume when the completeness == 1
    tsf= gaia_tools.select.tgasSelectUniform(comp=1.)
    tesf= gaia_tools.select.tgasEffectiveSelect(tsf)
    dxy, dz, zmin= 0.2, 0.1, 0.15
    v= tesf.volume(\
        lambda x,y,z: cyl_vol_func(x,y,z,xymax=dxy,zmin=zmin,zmax=zmin+dz),
        xyz=True)
    v_exp= numpy.pi*dxy**2.*dz
    assert(numpy.fabs(v/v_exp-1.) < 10.**-3.), 'Effective volume for unit completeness is not equal to the volume'
    # Another one
    dxy, dz, zmin= 0.2, 0.2, -0.15
    v= tesf.volume(\
        lambda x,y,z: cyl_vol_func(x,y,z,xymax=dxy,zmin=zmin,zmax=zmin+dz),
        xyz=True,ndists=251)
    v_exp= numpy.pi*dxy**2.*dz
    assert(numpy.fabs(v/v_exp-1.) < 10.**-2.), 'Effective volume for unit completeness is not equal to the volume'
    return None

def test_effvol_uniform_complete():
    # Test that the effective volume == A x volume when the completeness == A
    comp= 0.33
    tsf= gaia_tools.select.tgasSelectUniform(comp=comp)
    tesf= gaia_tools.select.tgasEffectiveSelect(tsf)
    dxy, dz, zmin= 0.2, 0.1, 0.15
    v= tesf.volume(\
        lambda x,y,z: cyl_vol_func(x,y,z,xymax=dxy,zmin=zmin,zmax=zmin+dz),
        xyz=True)
    v_exp= numpy.pi*dxy**2.*dz*comp
    assert(numpy.fabs(v/v_exp-1.) < 10.**-3.), 'Effective volume for unit completeness is not equal to the volume'
    # Another one
    dxy, dz, zmin= 0.2, 0.2, -0.15
    v= tesf.volume(\
        lambda x,y,z: cyl_vol_func(x,y,z,xymax=dxy,zmin=zmin,zmax=zmin+dz),
        xyz=True,ndists=251)
    v_exp= numpy.pi*dxy**2.*dz*comp
    assert(numpy.fabs(v/v_exp-1.) < 10.**-2.), 'Effective volume for unit completeness is not equal to the volume'
    return None

def test_effvol_uniform_complete_partialsky():
    # Test that the effective volume == A x volume x sky-fraction when the completeness == A over a fraction of the sky for a spherical volume
    comp= 0.33
    ramin, ramax= 30., 120.
    tsf= gaia_tools.select.tgasSelectUniform(comp=comp,ramin=ramin,ramax=ramax)
    tesf= gaia_tools.select.tgasEffectiveSelect(tsf)
    dr, rmin= 0.1, 0.
    v= tesf.volume(\
        lambda x,y,z: spher_vol_func(x,y,z,rmin=rmin,rmax=rmin+dr),
        xyz=True,ndists=251)
    v_exp= 4.*numpy.pi*dr**3./3.*comp*(ramax-ramin)/360.
    assert(numpy.fabs(v/v_exp-1.) < 10.**-2.), 'Effective volume for unit completeness is not equal to the volume'
    # Another one
    dr, rmin= 0.2, 0.
    v= tesf.volume(\
        lambda x,y,z: spher_vol_func(x,y,z,rmin=rmin,rmax=rmin+dr),
        xyz=True,ndists=501)
    v_exp= 4.*numpy.pi*dr**3./3.*comp*(ramax-ramin)/360.
    assert(numpy.fabs(v/v_exp-1.) < 10.**-1.9), 'Effective volume for unit completeness is not equal to the volume'
    return None

def test_effvol_uniform_complete_gaiagoodsky():
    # Test that the effective volume == A x volume x sky-fraction when the completeness == A over a fraction of the sky for a spherical volume
    comp= 0.33
    tsf= gaia_tools.select.tgasSelectUniform(comp=comp,keepexclude=True)
    tesf= gaia_tools.select.tgasEffectiveSelect(tsf)
    dr, rmin= 0.1, 0.
    v= tesf.volume(\
        lambda x,y,z: spher_vol_func(x,y,z,rmin=rmin,rmax=rmin+dr),
        xyz=True,ndists=251)
    v_exp= 4.*numpy.pi*dr**3./3.*comp\
        *float(numpy.sum(True-tsf._exclude_mask_skyonly))\
        /len(tsf._exclude_mask_skyonly)
    assert(numpy.fabs(v/v_exp-1.) < 10.**-2.), 'Effective volume for unit completeness is not equal to the volume'
    # Another one
    dr, rmin= 0.2, 0.
    v= tesf.volume(\
        lambda x,y,z: spher_vol_func(x,y,z,rmin=rmin,rmax=rmin+dr),
        xyz=True,ndists=501)
    v_exp= 4.*numpy.pi*dr**3./3.*comp\
        *float(numpy.sum(True-tsf._exclude_mask_skyonly))\
        /len(tsf._exclude_mask_skyonly)
    assert(numpy.fabs(v/v_exp-1.) < 10.**-1.9), 'Effective volume for unit completeness is not equal to the volume'
    return None

def cyl_vol_func(X,Y,Z,xymin=0.,xymax=0.15,zmin=0.05,zmax=0.15):
    """A function that bins in cylindrical annuli around the Sun"""
    xy= numpy.sqrt(X**2.+Y**2.)
    out= numpy.zeros_like(X)
    out[(xy >= xymin)*(xy < xymax)*(Z >= zmin)*(Z < zmax)]= 1.
    return out

def spher_vol_func(X,Y,Z,rmin=0.,rmax=0.15):
    """A function that bins in spherical annuli around the Sun"""
    r= numpy.sqrt(X**2.+Y**2.+Z**2.)
    out= numpy.zeros_like(X)
    out[(r >= rmin)*(r < rmax)]= 1.
    return out
