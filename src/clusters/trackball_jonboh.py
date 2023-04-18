from clusters.trackball_wilder import TrackballWild
from clusters.default_cluster import DefaultCluster
import json
import os

class TrackballJonboh(DefaultCluster):
    key_diameter = 75
    translation_offset = [
        -14,
        8,
        -7
    ]
    rotation_offset = [
        10,
        -5,
        0
    ]

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
                self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                # self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
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
                self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                # self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
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
        t1 = self.thumb_1x_layout(sa_cap(1))
        return t1


    def tb_post_r(self):
        debugprint('post_r()')
        radius = ball_diameter/2 + ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_tr(self):
        debugprint('post_tr()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_tl(self):
        debugprint('post_tl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_l(self):
        debugprint('post_l()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_bl(self):
        debugprint('post_bl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )


    def tb_post_br(self):
        debugprint('post_br()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(rotate(single_plate(side=side), (0, 0, -90)))
        shape = union([shape, self.thumb_15x_layout(rotate(single_plate(side=side), (0, 0, -90)))])
        # shape = union([shape, self.thumb_15x_layout(double_plate(), plate=False)])

        return shape


    def thumb_connectors(self, side="right"):
        print('default thumb_connectors()')
        hulls = []

        # Top two
        if default_1U_cluster:
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(web_post_tr()),
                        self.tl_place(web_post_br()),
                        self.tr_place(web_post_tl()),
                        self.tr_place(web_post_bl()),
                    ]
                )
            )
        else:
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(self.thumb_post_tr()),
                        self.tl_place(self.thumb_post_br()),
                        self.tr_place(self.thumb_post_tl()),
                        self.tr_place(self.thumb_post_bl()),
                    ]
                )
            )

        # bottom two on the right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                ]
            )
        )

        # bottom two on the left
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                ]
            )
        )
        # centers thumb cluster
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                    self.track_place(self.tb_post_br()),
                    self.tl_place(web_post_bl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_bl()),
                    self.br_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                    self.mr_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.tl_place(web_post_bl()),
                    self.tl_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                ]
            )
        )

        if default_1U_cluster:
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(web_post_tl()),
                        self.ml_place(web_post_tr()),
                        self.tl_place(web_post_bl()),
                        self.ml_place(web_post_br()),
                        self.tl_place(web_post_br()),
                        self.mr_place(web_post_tr()),
                        self.tr_place(web_post_bl()),
                        self.mr_place(web_post_br()),
                        self.tr_place(web_post_br()),
                    ]
                )
            )
        else:
            # top two to the main keyboard, starting on the left
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(self.thumb_post_tl()),
                        self.ml_place(web_post_tr()),
                        self.tl_place(self.thumb_post_bl()),
                        self.ml_place(web_post_br()),
                        self.tl_place(self.thumb_post_br()),
                        self.mr_place(web_post_tr()),
                        self.tr_place(self.thumb_post_bl()),
                        self.mr_place(web_post_br()),
                        self.tr_place(self.thumb_post_br()),
                    ]
                )
            )

        if default_1U_cluster:
            hulls.append(triangle_hulls(
                    [
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 0, cornerrow),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 1, cornerrow),
                        cluster_key_place(web_post_br(), 1, cornerrow),
                        cluster_key_place(web_post_bl(), 1, cornerrow),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 1, cornerrow),
                        cluster_key_place(web_post_bl(), 0, cornerrow),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 0, cornerrow),
                        ]
                ))
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(web_post_tl()),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 0, cornerrow),
                        self.tl_place(web_post_tr()),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 1, cornerrow),
                        self.tr_place(web_post_tl()),
                        cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 1, cornerrow),
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
        else:
            hulls.append(
                triangle_hulls(
                    [
                        self.tl_place(self.thumb_post_tl()),
                        cluster_key_place(web_post_bl(), 0, cornerrow),
                        self.tl_place(self.thumb_post_tr()),
                        cluster_key_place(web_post_br(), 0, cornerrow),
                        self.tr_place(self.thumb_post_tl()),
                        cluster_key_place(web_post_bl(), 1, cornerrow),
                        self.tr_place(self.thumb_post_tr()),
                        cluster_key_place(web_post_br(), 1, cornerrow),
                        cluster_key_place(web_post_tl(), 2, lastrow),
                        cluster_key_place(web_post_bl(), 2, lastrow),
                        self.tr_place(self.thumb_post_tr()),
                        cluster_key_place(web_post_bl(), 2, lastrow),
                        self.tr_place(self.thumb_post_br()),
                        cluster_key_place(web_post_br(), 2, lastrow),
                        cluster_key_place(web_post_bl(), 3, lastrow),
                        cluster_key_place(web_post_tr(), 2, lastrow),
                        cluster_key_place(web_post_tl(), 3, lastrow),
                        cluster_key_place(web_post_bl(), 3, cornerrow),
                        cluster_key_place(web_post_tr(), 3, lastrow),
                        cluster_key_place(web_post_br(), 3, cornerrow),
                        cluster_key_place(web_post_bl(), 4, cornerrow),
                    ]
                )
            )

        # hulls.append(
        #     triangle_hulls(
        #         [
        #             cluster_key_place(web_post_br(), 1, cornerrow),
        #             cluster_key_place(web_post_tl(), 2, lastrow),
        #             cluster_key_place(web_post_bl(), 2, cornerrow),
        #             cluster_key_place(web_post_tr(), 2, lastrow),
        #             cluster_key_place(web_post_br(), 2, cornerrow),
        #             cluster_key_place(web_post_bl(), 3, cornerrow),
        #         ]
        #     )
        # )

        # if not full_last_rows:
        #     hulls.append(
        #         triangle_hulls(
        #             [
        #                 cluster_key_place(web_post_tr(), 3, lastrow),
        #                 cluster_key_place(web_post_br(), 3, lastrow),
        #                 cluster_key_place(web_post_tr(), 3, lastrow),
        #                 cluster_key_place(web_post_bl(), 4, cornerrow),
        #             ]
        #         )
        #     )

        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        shapes = list()
        # thumb, walls
        if default_1U_cluster:
            shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, web_post_br()))
        else:
            shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, self.thumb_post_br()))
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.mr_place, 0, -1, web_post_bl()))
        shapes.append(wall_brace(self.br_place, 0, -1, web_post_br(), self.br_place, 0, -1, web_post_bl()))
        # shape = union([shape, wall_brace(self.ml_place, -0.3, 1, web_post_tr(), self.ml_place, 0, 1, web_post_tl())])
        # shape = union([shape, wall_brace(self.bl_place, 0, 1, web_post_tr(), self.bl_place, 0, 1, web_post_tl())])
        shapes.append(wall_brace(self.br_place, -1, 0, web_post_tl(), self.br_place, -1, 0, web_post_bl()))
        shapes.append(wall_brace(self.bl_place, -1, 0, web_post_tl(), self.bl_place, -1, 0, web_post_bl()))
        # thumb, corners
        shapes.append(wall_brace(self.br_place, -1, 0, web_post_bl(), self.br_place, 0, -1, web_post_bl()))
        shapes.append(wall_brace(self.bl_place, -1, 0, web_post_tl(), self.bl_place, 0, 1, web_post_tl()))
        # thumb, tweeners
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_bl(), self.br_place, 0, -1, web_post_br()))
        # shape = union([shape, wall_brace(self.ml_place, 0, 1, web_post_tl(), self.bl_place, 0, 1, web_post_tr())])
        shapes.append(wall_brace(self.bl_place, -1, 0, web_post_bl(), self.br_place, -1, 0, web_post_tl()))
        if default_1U_cluster:
            shapes.append( wall_brace(self.tr_place, 0, -1, web_post_br(), (lambda sh: cluster_key_place(sh, 4, lastrow)), 0,
                                      -1, web_post_bl()))
        else:
            shapes.append(wall_brace(self.tr_place, 0, -1, self.thumb_post_br(),
                                             (lambda sh: cluster_key_place(sh, 4, lastrow)), 0, -1, web_post_bl()))

        # TOP LEFT BEHIND TRACKBALL
        shapes.append(wall_brace(
            self.track_place, -2, 0, self.tb_post_tl(),
            (lambda sh: left_cluster_key_place(sh, lastrow - 2, -1, side=ball_side, low_corner=True)), -1, 0, web_post(),
        ))
        # LEFT OF TRACKBALL
        shapes.append(wall_brace(
            self.track_place, -2, 0, self.tb_post_tl(),
            self.track_place, -2, 0, self.tb_post_l(),
        ))
        shapes.append(wall_brace(
            self.track_place, -2, 0, self.tb_post_l(),
            self.bl_place, -1, 0, web_post_tl(),
        ))
        vertical = union(list(map(lambda x: x[0], shapes)))
        braces = union(list(map(lambda x: x[1], shapes)))
        return vertical, braces


    def connection(self, side='right'):
        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        # shape = union([bottom_hull(
        #     [
        #         left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
        #         left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
        #         self.ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
        #         self.ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
        #     ]
        # )])

        # shape = union([shape,
        #                bottom_hull(
        #             [
        #                 left_cluster_key_place(translate(web_post_tr(), wall_locate3(-0.3, 1)), cornerrow, -1, low_corner=True, side=side),
        #                 self.track_place(self.tb_post_tl()),
        #              ]
        #                    )])
        # Filling between BL and Trackball
        shape = hull_from_shapes([
            self.track_place(self.tb_post_l()),
            self.bl_place(web_post_tr()),
            self.bl_place(web_post_tl())
            ],
        )
        # Filling between left wall and trackball
        shape = union([shape, triangle_hulls([
            self.track_place(self.tb_post_tl()),
            self.tl_place(web_post_tl()),
            left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow-2, -1, low_corner=True, side=side),
            self.track_place(self.tb_post_tr()),
            left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow-1, -1, low_corner=True, side=side),
            self.track_place(self.tb_post_tr()),
            left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
            self.tl_place(web_post_tl()),
            cluster_key_place(web_post_bl(), 0, cornerrow),
            ])])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )
                       ])  # )

        shape = union([shape,
                        triangle_hulls([
                                cluster_key_place(web_post_bl(), 0, cornerrow),
                                cluster_key_place(translate(web_post_bl(), wall_locate1(0, -1)), 0, cornerrow),
                               self.tl_place(web_post_tl()),
                            ])
                       ])

        shape = union([shape, hull_from_shapes(
            [
                left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        shape = union([shape, hull_from_shapes(
            [
                left_cluster_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                key_place(web_post_bl(), 0, cornerrow),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        shape = union([shape, hull_from_shapes(
            [
                self.ml_place(web_post_tr()),
                self.ml_place(translate(web_post_tr(), wall_locate1(-0.3, 1))),
                self.ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
                self.ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        shape = union([shape, hull_from_shapes(
            [
                self.tl_place(self.thumb_post_tl()),
                cluster_key_place(web_post_bl(), 0, cornerrow),
                key_place(web_post_bl(), 0, cornerrow),
                # left_cluster_key_place(web_post_bl(), cornerrow, 0, low_corner=False, side=side),
                translate(key_place(web_post_bl(), 0, cornerrow), wall_locate1(-1, 0)),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        # shape = union([shape, key_place(sphere(5), 0, cornerrow)])

        return shape# print('thumb_connection()')

    # def screw_positions(self):
    #     position = self.thumborigin()
    #     position = list(np.array(position) + np.array([-72, -40, -16]))
    #     position[2] = 0
    #
    #     return position
    def has_btus(self):
        return True
