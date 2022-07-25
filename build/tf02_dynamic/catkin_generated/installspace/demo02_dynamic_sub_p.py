#!/usr/bin/env python3

# from ast import Expression
import rospy
import tf2_ros
from tf2_geometry_msgs import tf2_geometry_msgs
# from tf2_geometry_msgs import PointStamped
""" 
    订阅方实现:订阅坐标变换，传入被转换的坐标点，调用转换算法
    流程：
        1.导包
        2.初始化
        3.创建订阅对象
        4.组织被转换的坐标点
        5.转换逻辑实现,调用tf封装的算法
        6.输出结果
        7.spin()|spinonce()
 """
if __name__ == '__main__':
    rospy.init_node("static_sub_p")
    #创建订阅对象
    #3-1.创建缓存对象
    buffer = tf2_ros.Buffer()
    #3-2.创建订阅对象(将缓存传入)
    sub = tf2_ros.TransformListener(buffer)
    ps = tf2_geometry_msgs.PointStamped()
    #时间戳 ---0
    ps.header.stamp = rospy.Time()
    ps.header.frame_id = "turtle1"
    ps.point.x = 2.0
    ps.point.y = 3.0
    ps.point.z = 5.0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #转换实现
        try:
            ps_out = buffer.transform(ps,"world")
                
            rospy.loginfo("转换后的坐标：(%.2f,%.2f,%.2f),参考的坐标系：%s",
                    ps_out.point.x,
                    ps_out.point.y,
                    ps_out.point.z,
                    ps_out.header.frame_id)
        except Exception as e:
            rospy.logwarn("错误提示：%s", e)
        rate.sleep()


