# Blender add-ons for SMPL skeleton's poses and trans

There are two blender add-ons for SMPL skeleton's poses and trans.The first is for making an offline visual demo.The second is to make a live visual demo.

## Offline Motion Capture
Show one demo
![image](https://github.com/yanch2116/Blender-addons-for-SMPL/blob/master/sources/Dance.gif)

You need to follow these steps to use the first add-on.

1. Open a blender file and import the fbx file of a model with SMPL skeleton

> I downloaded a model on [Mixamo](https://www.mixamo.com) that happened to be an SMPL skeleton, and I changed the name of each bone so that the code could find the bones and act on them.You can find it in sources folder.

> 

> If you want to use your own model, make sure that the skeleton is SMPL skeleton and that the bones are named the same as in the code.

> Also, you need to change the name of model to Armature1.

1. Prepare the pkl file

> You need to prepare a pkl file, datas can be read by `pickling.load(f)['model']`, where f stands for pkl file. 

> Datas are lists of [N,75], where N stands for the number of frames.The 75 elements represent SMPL's poses and global translation.The first 72 elements are SMPL poses, and the last 3 elements are global translation.

> You then modify the file path in the code so that it can read your pkl file.

3. Install the addon-on
4. Make the skeleton and model active,then presh ctrl+R to run the add-on

Inserting keyframes takes a long time, you have to wait, and it's best not to insert more than 10000 frames at a time.

## Real Time Motion Capture

ROMP outputs SMPL's poses and trans more than 20 times per second. With ROMP and the plugin, the output of ROMP can be input into Blender's skeleton in real time to achieve the effect of human-driven animation characters.

Of course, every model that outputs SMPL's poses and trans can use this plugin to drive animation characters in Blender.
