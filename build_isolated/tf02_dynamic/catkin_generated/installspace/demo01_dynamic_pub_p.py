#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
import tf2_ros
from geometry_msgs.msg import TransformStamped
import tf_conversions
""" 
    发布方：订阅乌龟的位姿信息，转换成坐标系的相对关系，再发布
    准备：
        话题:/turtle1/pose
        类型：/turtlesim/Pose
    流程：
        1.导包
        2.初始化ros节点
        3.创建订阅对象
        4.回调函数处理订阅到的消息(核心)
        5.spin()
 """
def doPose(pose):
    #创建发布坐标系相对关系的对象
    pub = tf2_ros.TransformBroadcaster()
    #将pose位姿信息转化为坐标系相关关系消息
    ts = TransformStamped()
    ts.header.frame_id = "world"
    ts.header.stamp = rospy.Time.now()
    ts.child_frame_id = "turtle1"
    # 子级坐标系相对于父级坐标系的偏移量
    ts.transform.translation.x = pose.x
    ts.transform.translation.y = pose.y
    ts.transform.translation.z = 0

    # 四元数
    # 从欧拉角转换四元数
    qtn = tf_conversions.transformations.quaternion_from_euler(0,0,pose.theta)
    ts.transform.rotation.x = qtn[0]
    ts.transform.rotation.y = qtn[1]
    ts.transform.rotation.z = qtn[2]
    ts.transform.rotation.w = qtn[3]
    #发布
    pub.sendTransform(ts)

if __name__ == '__main__':
    # 1.初始化ros节点
    rospy.init_node("dynamic_pub_p")
    # 2.创建订阅对象
    sub = rospy.Subscriber("/turtle1/pose",Pose,doPose,queue_size=100)
    rospy.spin()