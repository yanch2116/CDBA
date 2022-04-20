from mathutils import Matrix, Vector, Quaternion,Euler
from math import radians
import numpy as np
import bpy

def getData():
    # Replace Your Own npz File PATH
    npz_path = '/Users/yanch/Desktop/CharacterDriven-BlenderAddon/demo/results.npz'
    a = np.load(
        npz_path, allow_pickle=True)['results'][()]
    data = []
    # results_ts.npz
    # for key in a[0]:
    #     data.append(a[0][key]['poses'])
    # results.npz

    for key in a:
        # temp = np.append(a[key][0]['poses'], a[key][0]['trans'])
        temp = np.append(a[key][0]['poses'], [0,0,0])
        data.append(temp)
    data = list(data)
    for i in range(len(data)):
        data[i] = list(data[i])
    return data


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

    def process_poses(self, mode, poses, trans, current_frame, pelvis_position):
        if not bpy.data.objects[0].parent:
            armature = bpy.data.objects[0]
        armature = bpy.data.objects[0].parent
        poses = np.array(poses)
        trans = np.array(trans)

        rod_rots = poses.reshape(24, 3)

        mat_rots = [self.Rodrigues(rod_rot) for rod_rot in rod_rots]

        bones = armature.pose.bones
        # bones[self.bone_name_from_index[0]].location = Vector((100*trans[1], 100*trans[2], 100*trans[0])) - pelvis_position
        bones[self.bone_name_from_index[0]].location = Vector((trans[1], trans[2], trans[0])) - pelvis_position
        if mode == 1:
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
            quat_y_90_cw = Quaternion((0.0, 1.0, 0.0), radians(180))
            quat_z_90_cw = Quaternion((0.0, 0.0, 1.0), radians(-90))

            if index == 0:
                # Rotate pelvis so that avatar stands upright and looks along negative Y avis
                bone.rotation_quaternion = (
                    quat_x_90_cw @ quat_z_90_cw) @ bone_rotation
            else:
                bone.rotation_quaternion = bone_rotation
            if mode == 1:
                bone.keyframe_insert(
                    'rotation_quaternion', frame=current_frame)
            bpy.context.scene.frame_end = current_frame

        return


class CharacterDriven(bpy.types.Operator):
    bl_idname = 'yanch.characterdriven'
    bl_label = 'characterdriven'

    def execute(self, ctx):
        poses = getData()
        SMPL_Importer_ = SMPL_Importer(ctx)
        pelvis_bone = bpy.data.armatures[0].bones['Pelvis']
        pelvis_position = Vector(pelvis_bone.head)
        i = 0
        for pose in poses:
            i += 1
            SMPL_Importer_.process_poses(
                1, pose[:72], pose[72:], i, pelvis_position)
        return {'FINISHED'}

addon_keymaps = []


def register():
    bpy.utils.register_class(CharacterDriven)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(
            name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            CharacterDriven.bl_idname, type='E', value='PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(CharacterDriven)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
