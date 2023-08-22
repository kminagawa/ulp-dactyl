from clusters.trackball_wilder import TrackballWild
from clusters.default_cluster import DefaultCluster
import json
import os

class TrackballJonboh(DefaultCluster):
    key_diameter = 75
    translation_offset = [
        -25,
        17,
        13
    ]
    rotation_offset = [
        25,
        7,
        22
    ]
    ball_wall_thickness = 2
    ball_gap = 5
    tb_height = -2

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

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        if cap:
            shape_list = [
                self.tl_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
                self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            ]

            if default_1U_cluster:
                shape_list.append(self.tr_place(rotate(rotate(shape, (0, 0, 90)), [0, 0, self.thumb_plate_tr_rotation])))
                shape_list.append(self.tr_place(rotate(rotate(shape, (0, 0, 90)), [0, 0, self.thumb_plate_tr_rotation])))
                shape_list.append(self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])))
            shapes = add(shape_list)

        else:
            shape_list = [
                self.tl_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
                self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            ]
            if default_1U_cluster:
                shape_list.append(self.tr_place(rotate(rotate(shape, (0, 0, 90)), [0, 0, self.thumb_plate_tr_rotation])))
            shapes = union(shape_list)
        return shapes

    def thumb_fx_layout(self, shape):
        return union([])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(choc_cap(1))
        return t1

    def tb_post(self, angle):
        radius = ball_diameter/2 + self.ball_wall_thickness + self.ball_gap
        return rotate(translate(web_post(), [radius - post_adj, 0, self.tb_height]),[0,0,angle])


    def tb_post_r(self):
        return self.tb_post(0)

    def tb_post_tr(self):
        return self.tb_post(60)


    def tb_post_tl(self):
        return self.tb_post(120)


    def tb_post_l(self):
        return self.tb_post(180)

    def tb_post_bl(self):
        return self.tb_post(240)


    def tb_post_br(self):
        return self.tb_post(300)

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(rotate(single_plate(side=side), (0, 0, -90)))
        shape = union([shape, self.thumb_15x_layout(rotate(single_plate(side=side), (0, 0, -90)))])
        # shape = union([shape, self.thumb_15x_layout(double_plate(), plate=False)])

        return shape


    def thumb_connectors(self, side="right"):
        print('default thumb_connectors()')
        hulls = []
        hulls.append(
            triangle_hulls(
                    [
                        self.tr_place(web_post_tl()),
                        self.tr_place(web_post_bl()),
                        self.mr_place(web_post_tr()),
                        self.mr_place(web_post_br())
                    ]
                )
            )
        hulls.append(
            triangle_hulls(
                [
                 self.tr_place(web_post_br()),
                 self.tr_place(web_post_bl()),
                 self.mr_place(web_post_br())
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_br()),
                    self.br_place(web_post_tr()),
                    self.mr_place(web_post_br()),
                    self.mr_place(web_post_bl())
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_bl()),
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_bl()),
                    self.bl_place(web_post_br()),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                    self.bl_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.bl_place(web_post_tr())
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.tl_place(web_post_bl()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_br()),
                    self.mr_place(web_post_tr()),
                    self.tr_place(web_post_tl())
                ]
                )
                )
        hulls.append(
            triangle_hulls(
                [
                    self.tr_place(web_post_tr()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_br()),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.tr_place(web_post_tr()),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(-1, -2)), 0, cornerrow),
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_tr()),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr()),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(-1, -2)), 0, cornerrow),
                    key_place(web_post_bl(), 0, 2),
                    self.tl_place(web_post_tr()),
                    key_place(web_post_tl(), 0, 2),
                ]
            ))
        hulls.append(triangle_hulls(
                [
                    cluster_key_place(translate(web_post_bl(), wall_locate1(-1, -2)), 0, cornerrow),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(0, -2)), 1, cornerrow),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 1, cornerrow),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(0, -2)), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(-1, -2)), 0, cornerrow),
                    ]
            ))
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(translate(web_post_bl(), wall_locate1(-1, -2)), 0, cornerrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(translate(web_post_br(), wall_locate1(0, -2)), 0, cornerrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(translate(web_post_bl(), wall_locate1(0, -2)), 1, cornerrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    self.tr_place(web_post_tr()),
                    self.tr_place(translate(web_post_tr(), wall_locate1(1, 0))),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    self.tr_place(translate(web_post_tr(), wall_locate1(1, 0))),
                    self.tr_place(translate(web_post_tr(), wall_locate1(1, 0))),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                    self.tr_place(translate(web_post_br(), wall_locate1(1, 0))),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                    self.tr_place(translate(web_post_br(), wall_locate1(1, 0))),
                    cluster_key_place(web_post_bl(), 4, cornerrow),
                    self.tr_place(translate(web_post_br(), wall_locate3(0, -1))),
                    self.tr_place(web_post_br()),
                    self.tr_place(translate(web_post_br(), wall_locate1(1, 0))),
                    self.tr_place(web_post_tr()),
                    self.tr_place(translate(web_post_tr(), wall_locate1(1, 0))),
                ]
            )
        )
        # hulls.append(triangle_hulls([
        #     self.bl_place(web_post_bl()),
        #     self.bl_place(web_post_tl()),
        #     self.track_place(translate(self.tb_post_bl(), wall_locate3(-4, 0))),
        #     self.track_place(translate(self.tb_post_tl(), wall_locate3(-4, 0))),
        #     ]))
        # hulls.append(triangle_hulls([
        #     self.bl_place(web_post_tl()),
        #     self.track_place(translate(self.tb_post_tl(), wall_locate3(-4, 0))),
        #     self.ml_place(web_post_tl())
        #     ]))
        # hulls.append(triangle_hulls([
        #     self.track_place(self.tb_post_tr()),
        #     self.track_place(translate(self.tb_post_tl(), wall_locate3(-4, 0))),
        #     left_key_place(web_post(), 1, -1, low_corner=True, side=side),
        #     ]))
        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        shapes = list()
        # thumb, walls
        shapes.append( wall_brace(self.tr_place, 0, -1, web_post_br(), (lambda sh: cluster_key_place(sh, 4, lastrow)), 0,
                                  -1, web_post_bl()))
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, web_post_br()))
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.br_place, 0, -1, web_post_br()))
        shapes.append(wall_brace(self.br_place, 0, -1, web_post_br(), self.br_place, -3, 0, web_post_bl()))
        shapes.append(wall_brace(self.br_place, -3, 0, web_post_bl(), self.bl_place, -3, 0, web_post_bl()))
        shapes.append(wall_brace(
                # lambda sh: left_key_place(translate(sh, wall_locate3(-1, 0)), 1, -1, low_corner=True, side=side),
                lambda sh: left_key_place(sh, 1, -1, low_corner=True, side=side),
                -1,0, web_post(),
                self.track_place,
                -3,0, translate(self.tb_post_tl(), wall_locate3(-4, 0)),
                ))
        shapes.append(wall_brace(
                # lambda sh: left_key_place(translate(sh, wall_locate3(-1, 0)), 1, -1, low_corner=True, side=side),
                self.track_place,
                -3,0, translate(self.tb_post_tl(), wall_locate3(-4, 0)),
                self.track_place,
                -3,0, translate(self.tb_post_bl(), wall_locate3(-4, 0)),
                ))
        shapes.append(wall_brace(
                self.track_place,
                -3,0, translate(self.tb_post_bl(), wall_locate3(-4, 0)),
                self.bl_place, -3, 0, web_post_bl()
                ))
        extra_walls = []
        extra_braces = []
        vertical = union(list(map(lambda x: x[0], shapes))+extra_walls)
        braces = union(list(map(lambda x: x[1], shapes))+extra_braces)
        return vertical, braces


    def connection(self, side='right'):
        print('thumb_connection()')
        shapes = list()
        shapes.append(triangle_hulls(
            [
                self.track_place(self.tb_post(30)),
                key_place(web_post_bl(), 0, 1),
                self.tl_place(web_post_tl()),
                self.tl_place(web_post_tr()),
                key_place(web_post_bl(), 0, 1),
            ]
            ))
        shapes.append(triangle_hulls(
            [
                self.tl_place(web_post_tr()),
                key_place(web_post_tl(), 0, 2),
                key_place(web_post_bl(), 0, 1),
            ]
            ))
        shapes.append(triangle_hulls([
                self.track_place(self.tb_post(30)),
                self.track_place(self.tb_post(60)),
                key_place(web_post_bl(), 0, 1),

            ]))
        shapes.append(triangle_hulls(
            [
                self.track_place(self.tb_post(120)),
                self.track_place(self.tb_post(90)),
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post(90)),
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post(60)),
                key_place(web_post_bl(), 0, 1),
                ]
            ))
        shapes.append(triangle_hulls(
            [
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                self.track_place(self.tb_post_tl()),
                self.track_place(translate(self.tb_post_tl(), wall_locate3(-4,0))),
                self.track_place(self.tb_post(150)),
                self.track_place(self.tb_post(180)),
                self.track_place(translate(self.tb_post_tl(), wall_locate3(-4,0))),
                self.track_place(translate(self.tb_post_bl(), wall_locate3(-4,0))),
                self.track_place(self.tb_post(210)),
                self.track_place(self.tb_post(240)),
                self.track_place(translate(self.tb_post_bl(), wall_locate3(-4,0))),
                self.track_place(self.tb_post(240)),
                self.bl_place(web_post_bl()),
                self.bl_place(web_post_tl()),
                self.track_place(self.tb_post(240)),
                self.bl_place(web_post_tr()),
                self.track_place(self.tb_post(270)),
                self.bl_place(web_post_tr()),
                self.track_place(self.tb_post(300)),
                self.tl_place(web_post_bl()),
                self.track_place(self.tb_post(330)),
                self.tl_place(web_post_tl()),
                self.track_place(self.tb_post(0)),
                self.tl_place(web_post_tl()),
                self.track_place(self.tb_post(30)),
                # self.tl_place(web_post_tl()),
                # self.track_place(self.tb_post(60))
            ]))
        # shapes.append(
        #     triangle_hulls(
        #             [
        #                 self.track_place(self.tb_post_tr()),
        #                 self.tl_place(web_post_tl()),
        #                 self.track_place(self.tb_post_r()),
        #                 self.tl_place(web_post_bl()),
        #                 self.track_place(self.tb_post_br()),
        #             ]
        #         )
        #     )
        # shapes.append(triangle_hulls([
        #             self.bl_place(web_post_tr()),
        #             self.bl_place(web_post_tl()),
        #             self.tl_place(web_post_bl()),
        #             self.track_place(self.tb_post_bl())
        #     ]))
        shape = union(shapes)

        return shape

    # def screw_positions(self):
    #     position = self.thumborigin()
    #     position = list(np.array(position) + np.array([-72, -40, -16]))
    #     position[2] = 0
    #
    #     return position
    def has_btus(self):
        return True
