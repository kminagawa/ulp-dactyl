from clusters.trackball_wilder import TrackballWild
from clusters.default_cluster import DefaultCluster
import json
import os


class TrackballJonboh(DefaultCluster):
    key_diameter = 75
    translation_offset = [
        -10,
        24,
        -27.25
    ]
    rotation_offset = [
        25,
        7,
        45
    ]
    ball_wall_thickness = 2
    ball_gap = 4
    tb_height = 0

    @staticmethod
    def name():
        return "TRACKBALL_JONBOH"

    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "DEFAULT.json"), mode='r') as fid:
            data = json.load(fid)

        superdata = super().get_config()

        # overwrite any super variables with this class' needs
        for item in data:
            superdata[item] = data[item]

        for item in superdata:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), superdata[item])

        return superdata

    def __init__(self, parent_locals):
        # self.num_keys = 4
        self.is_tb = True
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    def position_rotation(self):
        rot = [10, -15, 5]
        pos = self.thumborigin()
        pos[0] -= 1
        pos[1] -= 1
        pos[2] += 3.5
        # Changes size based on key diameter around ball, shifting off of the top left cluster key.
        shift = [-.9 * self.key_diameter/2 + 27 - 42, -.1 * self.key_diameter / 2 + 3 - 20, -5]
        for i in range(len(pos)):
            pos[i] = pos[i] + shift[i] + self.translation_offset[i]

        for i in range(len(rot)):
            rot[i] = rot[i] + self.rotation_offset[i]

        return pos, rot

    def track_place(self, shape):
        pos, rot = self.position_rotation()
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    def _thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        shapes = [
            self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
            self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
            self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation]))
        ]
        return shapes

    def thumb_fx_layout(self, shape):
        return union([])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(ulp_cap(1))
        return t1

    def tb_post(self, y_rotation, z_rotation):
        radius = ball_diameter/2 + self.ball_wall_thickness + self.ball_gap
        return rotate(translate(web_post(), [radius - post_adj, 0, self.tb_height]),[0,y_rotation,z_rotation])


    def tb_post_0(self):
        return self.tb_post(-20, 0)

    def tb_post_30(self):
        return self.tb_post(-20, 30)

    def tb_post_60(self):
        return self.tb_post(-15, 60)

    def tb_post_90(self):
        return self.tb_post(-10, 90)

    def tb_post_120(self):
        return self.tb_post(-10, 120)

    def tb_post_150(self):
        return self.tb_post(-10, 150)

    def tb_post_180(self):
        return self.tb_post(-10, 180)

    def tb_post_210(self):
        return self.tb_post(-10, 210)

    def tb_post_240(self):
        return self.tb_post(-20, 240)

    def tb_post_270(self):
        return self.tb_post(-20, 270)

    def tb_post_300(self):
        return self.tb_post(-20, 300)

    def tb_post_330(self):
        return self.tb_post(-20, 330)

    def _thumb_connectors(self, side="right"):
        hulls = []
        hulls += _triangle_hulls(
                [
                 self.tr_place(web_post_br()),
                 self.tr_place(web_post_bl()),
                 self.mr_place(web_post_br()),
                 self.tr_place(web_post_bl()),
                 self.mr_place(web_post_tr()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                    self.mr_place(web_post_tr()),
                    self.tr_place(web_post_tl())
                ]
                )
        hulls += _triangle_hulls(
                [
                    self.mr_place(web_post_bl()),
                    self.mr_place(web_post_tl()),
                    self.bl_place(web_post_tr()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.tl_place(web_post_br()),
                    self.tr_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.tr_place(web_post_tr()),
                    self.tr_place(web_post_tl()),
                    self.tl_place(web_post_br()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                ]
            )
        hulls += _triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_tr()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.tl_place(web_post_tr()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    key_place(web_post_bl(), 0, 2),
                    self.tl_place(web_post_tr()),
                    key_place(web_post_tl(), 0, 2),
                ]
            )
        hulls += _triangle_hulls(
                [
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_br(), 0, cornerrow),
                    self.tr_place(web_post_br()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.mr_place(web_post_bl()),
                    self.bl_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                ]
            )
        hulls += _triangle_hulls(
                [
                    self.mr_place(web_post_tr()),
                    self.tr_place(web_post_bl()),
                    self.tr_place(web_post_tl()),
                ]
            )
        return hulls

    def walls(self, side="right"):
        print('thumb_walls()')
        shapes = list()
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.mr_place, 0, -1, web_post_bl()))
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_bl(), self.bl_place, -3, -1, web_post_br()))
        shapes.append(wall_brace(self.bl_place, -3, -1, web_post_br(), self.bl_place, -3, -1, web_post_bl()))
        shapes.append(wall_brace(self.bl_place, -3, -1, web_post_bl(), self.bl_place, -3, 0, web_post_bl()))

        shapes.append(wall_brace(
                lambda sh: left_key_place(sh, 1, -1, low_corner=True, side=side),
                -1, 0, web_post(),
                self.track_place,
                -3, 0, translate(self.tb_post_120(), wall_locate3(-4, 0)),
                ))
        shapes.append(wall_brace(
                self.track_place,
                -3, 0, translate(self.tb_post_120(), wall_locate3(-4, 0)),
                self.track_place,
                -3, 0, translate(self.tb_post_240(), wall_locate3(-4, 2)),
                ))
        shapes.append(wall_brace(
                self.track_place,
                -3, 0, translate(self.tb_post_240(), wall_locate3(-4, 2)),
                self.bl_place,
                -3, 0, web_post_bl(),
                ))
        shapes.append(wall_brace((lambda sh: cluster_key_place(sh, 0, lastrow)), 0, -1, web_post_br(),
                                 (lambda sh: cluster_key_place(sh, 1, lastrow)), 0, -1, web_post_bl()))
        shapes.append(wall_brace((lambda sh: cluster_key_place(sh, 1, lastrow)), 0, -1, web_post_bl(),
                                 (lambda sh: cluster_key_place(sh, 1, lastrow)), 0, -1, web_post_br()))
        shapes.append(wall_brace((lambda sh: cluster_key_place(sh, 1, lastrow)), 0, -1, web_post_br(),
                                 (lambda sh: cluster_key_place(sh, 3, lastrow)), 0, -1, web_post_bl()))
        shapes.append(wall_brace((lambda sh: cluster_key_place(sh, 3, lastrow)), 0, -1, web_post_bl(),
                                 (lambda sh: cluster_key_place(sh, 3, lastrow)), -1, -1, web_post_br()))
        shapes.append(wall_brace((lambda sh: cluster_key_place(sh, 3, lastrow)), -1, -1, web_post_br(),
                                 self.br_place, -1, -1, web_post_tl()))
        shapes.append(wall_brace(self.br_place, -1, -1, web_post_tl(),
                                 self.br_place, -1, -1, web_post_bl()))
        shapes.append(wall_brace(self.br_place, -1, -1, web_post_bl(),
                                 self.br_place, 1, -1, web_post_br()))
        shapes.append(wall_brace( self.br_place, 1, -1, web_post_br(),
                                 (lambda sh: cluster_key_place(sh, 4, lastrow)), 1, 0, web_post_br()))
        # thumb corner
        extra_walls = [
                bottom_hull(_triangle_hulls([
                    self.tr_place(web_post_bl()),
                    self.tr_place(translate(web_post_bl(), wall_locate1(0,-1))),
                    self.tr_place(web_post_br()),
                    self.tr_place(translate(web_post_bl(), wall_locate1(0,-1))),
                    self.tr_place(web_post_br()),
                    self.tr_place(translate(web_post_bl(), wall_locate3(0,-1))),
                    ])),
bottom_hull(_triangle_hulls([
                    self.tr_place(web_post_bl()),
                    self.tr_place(translate(web_post_bl(), wall_locate1(0,-1))),
                    self.tr_place(web_post_br()),
                    self.tr_place(translate(web_post_bl(), wall_locate1(0,-1))),
                    self.tr_place(web_post_br()),
                    self.tr_place(translate(web_post_bl(), wall_locate3(0,-1))),
                    ]))
                ]
        extra_braces = []
        vertical = union(list(map(lambda x: x[0], shapes))+extra_walls)
        braces = union(list(map(lambda x: x[1], shapes))+extra_braces)
        return vertical, braces


    def connection(self, side='right'):
        print('thumb_connection()')
        shapes = list()
        shapes.append(triangle_hulls(
            [
                self.tl_place(web_post_tr()),
                key_place(web_post_tl(), 0, 2),
                key_place(web_post_bl(), 0, 1),
            ]
            ))
        shapes.append(triangle_hulls(
            [
                self.track_place(self.tb_post_30()),
                key_place(web_post_bl(), 0, 1),
                self.tl_place(web_post_tl()),
                self.tl_place(web_post_tr()),
                key_place(web_post_bl(), 0, 1),
            ]
        ))
        shapes.append(triangle_hulls([
                self.track_place(self.tb_post_60()),
                self.track_place(self.tb_post_30()),
                key_place(web_post_bl(), 0, 1),
            ]))
        shapes.append(triangle_hulls(
            [
                self.track_place(self.tb_post_120()),
                self.track_place(self.tb_post_90()),
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post_90()),
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post_60()),
                key_place(web_post_bl(), 0, 1),
                ]
            ))
        shapes.append(triangle_hulls(
            [
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post_120()),
                self.track_place(translate(self.tb_post_120(), wall_locate3(-4,0))),
                self.track_place(self.tb_post_150()),
                self.track_place(self.tb_post_180()),
                self.track_place(translate(self.tb_post_120(), wall_locate3(-4,0))),
                self.track_place(translate(self.tb_post_240(), wall_locate3(-4,2))),
                self.track_place(self.tb_post_210()),
                self.track_place(translate(self.tb_post_240(), wall_locate3(-4,2))),
                self.track_place(self.tb_post_210()),
                self.bl_place(web_post_tl()),
                self.track_place(self.tb_post_240()),
                self.bl_place(web_post_tl()),
                self.track_place(self.tb_post_240()),
                self.bl_place(web_post_tr()),
                self.track_place(self.tb_post_270()),
                self.tl_place(web_post_bl()),
                self.track_place(self.tb_post_300()),
                self.tl_place(web_post_bl()),
                self.track_place(self.tb_post_300()),
                self.tl_place(web_post_tl()),
                self.track_place(self.tb_post_330()),
                self.tl_place(web_post_tl()),
                self.track_place(self.tb_post_0()),
                self.tl_place(web_post_tl()),
                self.track_place(self.tb_post_30()),
            ]))
        shapes.append(triangle_hulls(
            [
                self.track_place(translate(self.tb_post_240(), wall_locate3(-4,2))),
                self.bl_place(web_post_tl()),
                self.bl_place(web_post_bl()),
                ]
            ))
        shape = union(shapes)

        return shape

    def has_btus(self):
        return True
