import enum
class Move_Const(enum.Enum):
    vx_shotgun=6
    vx_machine_gun=4
    vx=7
    vy=9
    zero=0
    g=0.15

class Orientation(enum.Enum):
    Left="Left"
    Right="Right"
    UpRight="UpRight"
    UpLeft="UpLeft"
    Down="Down"
    Non="None"
    Space="Space"
    Bullet_Right_move="Bullet_Right_move"
    Bullet_Left_move="Bullet_Left_move"
    Bullet_Left_stand="Bullet_Left_stand"
    Bullet_Right_stand = "Bullet_Right_stand"
    Bullet_stand = "Bullet_stand"
    Death="Death"

class Guns(enum.Enum):
    machine_gun="machine_gun"
    shotgun="shotgun"

class Animation_const(enum.Enum):
    machine_gun=8
    shotgun=11