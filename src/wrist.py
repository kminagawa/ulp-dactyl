import solid2 as s

from catmull import catmull_rom_chain

def catmull_points(points, npoints):
    cr_points_ = catmull_rom_chain(points, npoints)
    cr_points = [points[0]]
    for point in cr_points_:
        cr_points.append(point)
    cr_points.append(points[-1])
    return cr_points

NPOINTS=10

def section(h):
    points = [
        (0,0*h),
        (4,5*h),
        (12,12*h),
        (16,15*h),
        (24,20*h),
        (32,23*h),
        (40,25*h),
        (54,26*h),
        (84,26.5*h),
        ]
    cr_points = catmull_points(points, NPOINTS)
    cr_points.append((84,0))
    return s.linear_extrude(height=1)(s.polygon(cr_points))

def rotation():
    points = [
        (0,0),
        (27,-0.5),
        (50,-2),
        (75,-4),
        (90,-7),
        ]
    return catmull_points(points, NPOINTS)

def scaling():
    points = [
        (0,0.95),
        (20,1.0),
        (27,1.02),
        (50,1.015),
        (75,1.01),
        (90,1),
        ]
    return catmull_points(points, NPOINTS)

def chained_hull(pieces):
    hulls = list()
    for i in range(len(pieces)-1):
        p0 = pieces[i]
        p1 = pieces[i+1]
        hulls.append(s.hull()(p0, p1))
    return s.union()(*hulls)

def wrist_rest(side="right"):
    height_scale = 0.8
    pieces = [s.translate([0,0, rot[0]])(s.rotate([0,0,rot[1]])(section(height_scale*scal[1]))) for rot, scal in zip(rotation(), scaling())]
    body = chained_hull(pieces)
    tear_hole_height = 1.5
    tear_hole_radius = 4.5
    silicone_hole = s.translate([tear_hole_radius, tear_hole_height-0.01, tear_hole_radius ])(s.rotate([90,0,0])(s.cylinder(h=tear_hole_height, r=tear_hole_radius)))
    silicone_holes = [
            s.translate([3.5, 0, 1.5])(silicone_hole),
            s.translate([3.5, 0, -1.5+90-2*tear_hole_radius])(silicone_hole),
            s.translate([1.5+63, 0, -1.5+90-2*tear_hole_radius])(silicone_hole),
            s.translate([1.5+63, 0, 1.5])(silicone_hole),
            ]

    body = s.difference()(body, *silicone_holes)
    body = s.difference()(body, s.translate([0, -200, 0])(s.cube([200,200,200])))
    return body

if __name__ == "__main__":
    right = wrist_rest()
    s.scad_render_to_file(right, "things/uncut_wrist_right.scad")
