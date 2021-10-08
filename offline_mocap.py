from mathutils import Matrix, Vector, Quaternion
from math import radians
import numpy as np
import pickle
import bpy


class MultiPerson(bpy.types.Operator):
    bl_idname = 'jd.importposes'
    bl_label = 'multiperson'
    path = '/Users/yanch/Downloads/results.pkl'
    frame = 0

    def execute(self, ctx):

        SMPL_Importer_ = SMPL_Importer(ctx)

        # You should change codes here to use your own data.
        f = open(self.path, 'rb')
        data = pickle.load(f)['model']
        num_frames = len(data)
        for frame in range(num_frames):
            self.frame += 1
            poses = data[frame][:72]
            trans = data[frame][72:75]
            SMPL_Importer_.process_poses(poses, trans, 1, self.frame)

        # data = np.load(self.npz_path, allow_pickle=True)['results'][()]
        # for key in data:
        #     self.frame += 1
        #     poses = data[key]['poses']
        #     trans = data[key]['trans']
        #     SMPL_Importer_.process_poses(poses,trans,1,self.frame)
        # for key in data[1]:
        #     self.frame += 1
        #     for pid in data.keys():
        #         if key in data[pid]:
        #             poses = data[pid][key]['poses']
        #             trans = data[pid][key]['trans']
        #             SMPL_Importer_.process_poses(poses, trans, pid, self.frame)

        return {'FINISHED'}


class SMPL_Importer:

    def __init__(self, context):

        self.bone_name_from_index = {
            0: 'Pelvis',
            1: 'L_Hip',
            2: 'R_Hip',
            3: 'Spine1',
            4: 'L_Knee',
            5: 'R_Knee',
            6: 'Spine2',
            7: 'L_Ankle',
            8: 'R_Ankle',
            9: 'Spine3',
            10: 'L_Foot',
            11: 'R_Foot',
            12: 'Neck',
            13: 'L_Collar',
            14: 'R_Collar',
            15: 'Head',
            16: 'L_Shoulder',
            17: 'R_Shoulder',
            18: 'L_Elbow',
            19: 'R_Elbow',
            20: 'L_Wrist',
            21: 'R_Wrist',
            22: 'L_Hand',
            23: 'R_Hand'
        }

    def Rodrigues(self, rotvec):
        theta = np.linalg.norm(rotvec)
        r = (rotvec/theta).reshape(3, 1) if theta > 0. else rotvec
        cost = np.cos(theta)
        mat = np.asarray([[0, -r[2], r[1]],
                          [r[2], 0, -r[0]],
                          [-r[1], r[0], 0]])
        return(cost*np.eye(3) + (1-cost)*r.dot(r.T) + np.sin(theta)*mat)

    def process_poses(self, poses, trans, pid, frame):
        scene = bpy.data.scenes['Scene']
        armature = bpy.data.objects['Armature%s' % pid]

        bpy.ops.object.mode_set(mode='EDIT')
        pelvis_bone = armature.data.edit_bones[self.bone_name_from_index[0]]
        pelvis_position = Vector(pelvis_bone.head)
        bpy.ops.object.mode_set(mode='OBJECT')
        self.process_pose(poses, trans,
                          frame, pelvis_position, armature)

    def process_pose(self, poses, trans, current_frame, pelvis_position, armature):
        poses = np.array(poses)
        trans = np.array(trans)

        if poses.shape[0] == 72:
            rod_rots = poses.reshape(24, 3)
        else:
            rod_rots = poses.reshape(26, 3)

        mat_rots = [self.Rodrigues(rod_rot) for rod_rot in rod_rots]

        bones = armature.pose.bones
        bones[self.bone_name_from_index[0]].location = Vector(
            (100*trans[1], 100*trans[2], 100*trans[0])) - pelvis_position
        bones[self.bone_name_from_index[0]].keyframe_insert(
            'location', frame=current_frame)

        for index, mat_rot in enumerate(mat_rots, 0):
            if index >= 24:
                continue

            bone = bones[self.bone_name_from_index[index]]

            bone_rotation = Matrix(mat_rot).to_quaternion()

            quat_x_90_cw = Quaternion((1.0, 0.0, 0.0), radians(-90))
            quat_x_n135_cw = Quaternion((1.0, 0.0, 0.0), radians(-135))
            quat_x_p45_cw = Quaternion((1.0, 0.0, 0.0), radians(45))
            quat_y_90_cw = Quaternion((0.0, 1.0, 0.0), radians(-90))
            quat_z_90_cw = Quaternion((0.0, 0.0, 1.0), radians(-90))

            if index == 0:
                # Rotate pelvis so that avatar stands upright and looks along negative Y avis
                bone.rotation_quaternion = (
                    quat_x_90_cw @ quat_z_90_cw) @ bone_rotation
            else:
                bone.rotation_quaternion = bone_rotation

            bone.keyframe_insert('rotation_quaternion', frame=current_frame)

        return


addon_keymaps = []


def register():

    bpy.utils.register_class(MultiPerson)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(
            name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            MultiPerson.bl_idname, type='R', value='PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.register_class(MultiPerson)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
