import json
import os


class DefaultCluster(object):
    num_keys = 6
    is_tb = False
    thumb_offsets = [
        8,
        0,
        9
    ]
    thumb_plate_tr_rotation = 0
    thumb_plate_tl_rotation = 0
    thumb_plate_mr_rotation = 0
    thumb_plate_ml_rotation = 0
    thumb_plate_br_rotation = 0
    thumb_plate_bl_rotation = 0

    @staticmethod
    def name():
        return "DEFAULT"


    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "DEFAULT.json"), mode='r') as fid:
            data = json.load(fid)
        for item in data:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), data[item])
        return data

    def __init__(self, parent_locals):
        for item in parent_locals:
            globals()[item] = parent_locals[item]
        self.get_config()
        print(self.name(), " built")

    def thumborigin(self):
        # debugprint('thumborigin()')
        origin = key_position([mount_width / 2, -(mount_height / 2), 0], 1, cornerrow)
        _thumb_offsets = self.thumb_offsets.copy()
        if shift_column != 0:
            _thumb_offsets[0] = self.thumb_offsets[0] + (shift_column * (mount_width + 6))
            # if shift_column < 0:  # raise cluster up when moving inward
            #     _thumb_offsets[1] = self.thumb_offsets[1] - (shift_column * 3)
            #     _thumb_offsets[2] = self.thumb_offsets[2] - (shift_column * 8)
            #     if shift_column <= -2:
            #         # y = shift_column * 15
            #         _thumb_offsets[1] = self.thumb_offsets[1] - (shift_column * 15)
        for i in range(len(origin)):
            origin[i] = origin[i] + _thumb_offsets[i]

        return origin

    def thumb_rotate(self):
        x = y = z = 0
        if shift_column != 0:
            y = shift_column * 8
            if shift_column < 0:
                z = shift_column * -10
        return [x, y, z]

    def thumb_place(self, shape):
        shape = translate(shape, self.thumborigin())
        return rotate(shape, self.thumb_rotate())

    def tl_place(self, shape):
        debugprint('tl_place()')
        shape = rotate(shape, [27.5, -18, 10])
        shape = translate(shape, [-42.5, 1, 15])
        shape = self.thumb_place(shape)
        return shape

    def tr_place(self, shape):
        debugprint('tr_place()')
        shape = rotate(shape, [10, -15, 10])
        shape = translate(shape, [-15, -17, 10])
        shape = self.thumb_place(shape)
        return shape

    def mr_place(self, shape):
        debugprint('mr_place()')
        # shape = rotate(shape, [-6, -34, 48])
        # shape = translate(shape, [-29, -40, -13])
        shape = rotate(shape, [7.5, -18, 10])
        shape = translate(shape, [-33.5, -22.5, 5.5])
        shape = self.thumb_place(shape)
        return shape

    def ml_place(self, shape):
        debugprint('ml_place()')
        # shape = rotate(shape, [6, -34, 10])
        # shape = translate(shape, [-51, -25, -12])
        shape = rotate(shape, [30.5, -22, 30])
        shape = translate(shape, [-64.5, -5, 10])
        shape = self.thumb_place(shape)
        return shape

    def br_place(self, shape):
        debugprint('br_place()')
        shape = rotate(shape, [6, -20, 10])
        shape = translate(shape, [-32, -44, -9])
        # shape = rotate(shape, [-16, -33, 54])
        # shape = translate(shape, [-37.8, -55.3, -25.3])
        shape = self.thumb_place(shape)
        return shape

    def bl_place(self, shape):
        debugprint('bl_place()')
        # shape = rotate(shape, [-4, -35, 52])
        # shape = translate(shape, [-56.3, -43.3, -23.5])
        shape = rotate(shape, [6, 0, 17])
        shape = translate(shape, [-55, -28, -5])
        shape = self.thumb_place(shape)
        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        if cap:
            shape_list = [
                self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
                self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
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
                self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
                self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
                self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            ]
            if default_1U_cluster:
                shape_list.append(self.tr_place(rotate(rotate(shape, (0, 0, 90)), [0, 0, self.thumb_plate_tr_rotation])))
            shapes = union(shape_list)
        return shapes

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        debugprint('thumb_15x_layout()')
        if plate:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                cap_list = [self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation]))]
                cap_list.append(self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])))
                return add(cap_list)
            else:
                shape_list = [self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation]))]
                if not default_1U_cluster:
                    shape_list.append(self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])))
                return union(shape_list)
        else:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                shape_list = [
                    self.tl_place(shape),
                ]
                shape_list.append(self.tr_place(shape))

                return add(shape_list)
            else:
                shape_list = [
                    self.tl_place(shape),
                ]
                if not default_1U_cluster:
                    shape_list.append(self.tr_place(shape))

                return union(shape_list)

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(dsa_cap(1), cap=True)
        if not default_1U_cluster:
            t1.add(self.thumb_15x_layout(dsa_cap(1.5), cap=True))
        return t1

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(rotate(single_plate(side=side), (0, 0, -90)))
        shape = union([shape, self.thumb_15x_layout(rotate(single_plate(side=side), (0, 0, -90)))])
        # shape = union([shape, self.thumb_15x_layout(double_plate(), plate=False)])

        return shape

    def thumb_post_tr(self):
        debugprint('thumb_post_tr()')
        return translate(web_post(),
                         [(mount_width / 2) - post_adj, ((mount_height / 2) + double_plate_height) - post_adj, 0]
                         )

    def thumb_post_tl(self):
        debugprint('thumb_post_tl()')
        return translate(web_post(),
                         [-(mount_width / 2) + post_adj, ((mount_height / 2) + double_plate_height) - post_adj, 0]
                         )

    def thumb_post_bl(self):
        debugprint('thumb_post_bl()')
        return translate(web_post(),
                         [-(mount_width / 2) + post_adj, -((mount_height / 2) + double_plate_height) + post_adj, 0]
                         )

    def thumb_post_br(self):
        debugprint('thumb_post_br()')
        return translate(web_post(),
                         [(mount_width / 2) - post_adj, -((mount_height / 2) + double_plate_height) + post_adj, 0]
                         )

    def thumb_connectors(self, side="right"):
        print('default thumb_connectors()')
        hulls = []
        hulls.append(
            triangle_hulls(
                    [
                        self.tl_place(web_post_tl()),
                        self.tl_place(web_post_bl()),
                        self.ml_place(web_post_tr()),
                        self.ml_place(web_post_br())
                    ]
                )
            )
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
                    self.bl_place(web_post_tl()),
                    self.bl_place(web_post_tr()),
                    self.ml_place(web_post_bl()),
                    self.ml_place(web_post_br()),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.ml_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                    self.mr_place(web_post_tr()),
                    self.tl_place(web_post_br())
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
        # hulls.append(
        #     triangle_hulls(
        #         [
        #
        #         ]))
        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        shapes = list()
        # thumb, walls
        if default_1U_cluster:
            shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, web_post_br()))
        else:
            shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, self.thumb_post_br()))
        shapes.append(wall_brace(self.mr_place, 0, -1, web_post_br(), self.br_place, 0, -1, web_post_br()))
        shapes.append(wall_brace(self.br_place, 0, -1, web_post_br(), self.br_place, -3, 0, web_post_bl()))
        shapes.append(wall_brace(self.br_place, -3, 0, web_post_bl(), self.bl_place, -3, 0, web_post_bl()))
        shapes.append(wall_brace(self.bl_place, -3, 0, web_post_bl(), self.bl_place, -3, 0, web_post_tl()))
        shapes.append(wall_brace(self.bl_place, -3, 0, web_post_tl(), self.ml_place, -3, 0, web_post_bl()))
        shapes.append(wall_brace(self.ml_place, -3, 0, web_post_bl(), self.ml_place, -3, 0, web_post_tl()))
        shapes.append( wall_brace(self.tr_place, 0, -1, web_post_br(), (lambda sh: cluster_key_place(sh, 4, lastrow)), 0,
                                  -1, web_post_bl()))
        shapes.append(wall_brace(
                # lambda sh: left_key_place(translate(sh, wall_locate3(-1, 0)), 1, -1, low_corner=True, side=side),
                lambda sh: left_key_place(sh, 1, -1, low_corner=True, side=side),
                -1,0, web_post(),
                self.ml_place,
                -3,0, web_post_tl(),
                ))
        extra_walls = []
        extra_braces = []
        vertical = union(list(map(lambda x: x[0], shapes))+extra_walls)
        braces = union(list(map(lambda x: x[1], shapes))+extra_braces)
        return vertical, braces

    def connection(self, side='right'):
        print('thumb_connection()')
        shapes = list()
        shapes.append(triangle_hulls([
                self.tl_place(web_post_tl()),
                self.ml_place(web_post_tr()),
                key_place(web_post_bl(), 0, 1),
                ]))
        shapes.append(triangle_hulls(
            [
                self.tl_place(web_post_tr()),
                key_place(web_post_tl(), 0, 2),
                key_place(web_post_bl(), 0, 1),
            ]
            ))
        shapes.append(triangle_hulls(
            [
                key_place(web_post_bl(), 0, 1),
                self.tl_place(web_post_tl()),
                self.tl_place(web_post_tr()),
                key_place(web_post_bl(), 0, 1),
            ]
            ))
        # shapes.append(triangle_hulls(
        #     [
        #         self.tl_place(web_post_tr()),
        #         key_place(web_post_tl(), 0, 2),
        #         key_place(web_post_bl(), 0, 1),
        #     ]
        #     ))
        shapes.append(triangle_hulls(
            [
                self.ml_place(web_post_tl()),
                self.ml_place(web_post_tr()),
                left_key_place(web_post(), 1, -1, low_corner=True, side=side),
                key_place(web_post_bl(), 0, 1),
                ]
            ))
        shape = union(shapes)

        return shape

    def screw_positions(self):
        position = self.thumborigin()
        position = list(np.array(position) + np.array([-15, -58, 0]))
        position[2] = 0

        return position

    def get_extras(self, shape, pos):
        return shape

    def has_btus(self):
        return False
