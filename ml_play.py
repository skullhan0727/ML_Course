"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)


def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    #不要改
    comm.ml_ready()


    ball_x=0
    ball_y=0
    should_x=75


    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        #遊戲場景資訊
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:

            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True
        else:
            #重點
            #一個frame放一個!! 不能沒有
            #打在else
            #ball 移動範圍 x:0~195 y:395 size:5*5
            #platform 移動範圍 x:0~160 y:400   size:5*40

            
            ball_x_old=ball_x
            ball_y_old=ball_y


            ball_x=scene_info.ball[0]
            ball_y=scene_info.ball[1]

            platform_x=scene_info.platform[0]
            platform_y=scene_info.platform[1]
            #print("x change:",ball_x-ball_x_old,"y change",ball_y-ball_y_old)

            if ball_y-ball_y_old>0 and 100<ball_y<190 :
                if ball_x-ball_x_old<0 :
                    hit_y=ball_y+(((ball_x-0)//7)+1)*7
                    if 395-hit_y<195:
                        should_x=0+(395-hit_y)
                    else:
                        should_x=195-((395-hit_y)-(195//7+1)*7)

                elif ball_x-ball_x_old>0:
                    hit_y=ball_y+(((195-ball_x)//7)+1)*7
                    if 395-hit_y<195:
                        should_x=195-(395-hit_y)
                    else:
                        should_x=0+((395-hit_y)-(195//7+1)*7)
              
           
            if ball_y-ball_y_old>0:
                if should_x<platform_x:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        #print("left")
                elif should_x>platform_x+30:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        #print("right")
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            print("ball_x",ball_x,"ball_y",ball_y,"should_x:",should_x,"platform_x:",platform_x) 

            if ball_y==395:
                print("************ball_x:",ball_x,"ball_y",ball_y,"platformx:",platform_x)









        
        
        
