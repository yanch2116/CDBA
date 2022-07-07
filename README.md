# CharacterDriven-BlenderAddon

The addon drives a 3D cartoon character by transferring SMPL's pose and global translation into the skeleton of the 3D character. Poses and global translation can be obtained from RGB images using ROMP or any SMPL-based 3D pose estimation model. If the estimation model outputs pose and global position at a high speed, then you can achieve the effect of driving 3D characters in real time in Blender.

## Two Pipeline

### From Video to Animation

![image](demo/demo1.gif)

Steps:

1. Modify the path of [results.npz](demo/results.npz) in [server.py](src/server.py) and start server.py in the command line.
2. Open [Beta.blend](blender/Beta.blend) or [SMPL.blend](blender/SMPL.blend) and click on the triangle in the upper right corner.If a message is displayed in the lower left corner, the addon is running successfully.
   ![图 2](images/c52b11b344f633d7d60dd2c3a4fd8af0057c2a873f5868227e5c3e3b6c27b37f.png)
3. Go back to the Layout view and click on the small icon in the upper right to get the Texture.
   ![图 1](images/bc3d69615afb7829359475a04e4dd024732f8a70736b7433a7aaf93888dc2be7.png)
4. Press Ctrl+E to run the addon. At this time, the keyframe that is being transferred is displayed in the command line running server.py.
   ![图 4](images/1a7a853daa25f17230482437550e1d94f22252f0b02807ab105eeb6a2bd8ae30.png)
5. Press the space in Blender to view the character animation.

> If you want to use your own video, you need to use [ROMP](https://github.com/Arthur151/ROMP)'s [video.sh](https://github.com/Arthur151/ROMP/blob/master/scripts/video.sh) to get a npz file.

### The Webcam Drive Character in Real-Time

![image](demo/demo2.gif)

Steps:

1. Connect the camera and run ROMP's [webcam_blender.sh](https://github.com/Arthur151/ROMP/blob/master/scripts/webcam_blender.sh).
2. The rest of the steps are the same as steps 2, 3 of `From Video to Animation`, where the 3D characters in Blender are driven in real time by pressing Ctrl+E.Press A to stop it.

## To Do

- [ ] Write an UI
- [ ] Make a video explaining how to use your own 3D characters
- [ ] Write the sending interface for ROMP or BEV

## Acknowledgement

- 3D character is downloaded from [Mixamo](https://www.mixamo.com/#/)
- [neuron_mocap_live-blender](https://github.com/pnmocap/neuron_mocap_live-blender)
- [QuickMocap-BlenderAddon](https://github.com/vltmedia/QuickMocap-BlenderAddon)
