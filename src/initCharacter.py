import bpy

name_changed = False
armature = bpy.data.armatures['Armature']
for bone in armature.bones:
    if bone.name == 'Pelvis':
        name_changed = True
        break
if not name_changed:
    bones_mixamo = {
        'Hips': 'Pelvis',
        'LeftUpLeg': 'L_Hip',
        'RightUpLeg': 'R_Hip',
        'Spine2': 'Spine3',
        'Spine1': 'Spine2',
        'Spine': 'Spine1',
        'LeftLeg': 'L_Knee',
        'RightLeg': 'R_Knee',
        'LeftFoot': 'L_Ankle',
        'RightFoot': 'R_Ankle',
        'LeftToeBase': 'L_Foot',
        'RightToeBase': 'R_Foot',
        'Neck': 'Neck',
        'LeftShoulder': 'L_Collar',
        'RightShoulder': 'R_Collar',
        'Head': 'Head',
        'LeftArm': 'L_Shoulder',
        'RightArm': 'R_Shoulder',
        'LeftForeArm': 'L_Elbow',
        'RightForeArm': 'R_Elbow',
        'LeftHand': 'L_Wrist',
        'RightHand': 'R_Wrist',
        'LeftHandIndex1': 'L_Hand',
        'LeftHandMiddle1': 'L_Hand',
        'RightHandMiddle1': 'R_Hand',
        'RightHandIndex1': 'R_Hand',
    }
    for key in bones_mixamo:
        for bone in armature.bones:
            if key in bone.name:
                bone.name = bones_mixamo[key]
                break

object = bpy.data.objects['Armature']
bones = ['Pelvis', 'L_Hip', 'R_Hip', 'Spine1', 'L_Knee', 'R_Knee', 'Spine2', 'L_Ankle', 'R_Ankle', 'Spine3', 'L_Foot', 'R_Foot',
         'Neck', 'L_Collar', 'R_Collar', 'Head', 'L_Shoulder', 'R_Shoulder', 'L_Elbow', 'R_Elbow', 'L_Wrist', 'R_Wrist', 'L_Hand', 'R_Hand']
bpy.ops.object.mode_set(mode='EDIT')
for bone in bones:
    object.data.edit_bones[bone].use_connect = False
for bone in bones:
    object.data.edit_bones[bone].tail[0] = object.data.edit_bones[bone].head[0]
    object.data.edit_bones[bone].tail[1] = object.data.edit_bones[bone].head[1]+2
    object.data.edit_bones[bone].tail[2] = object.data.edit_bones[bone].head[2]
    object.data.edit_bones[bone].roll = 0
bpy.ops.object.mode_set(mode='OBJECT')
