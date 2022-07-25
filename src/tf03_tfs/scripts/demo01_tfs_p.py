#! /usr/bin/env python

import rospy
import tf2_ros
from tf2_geometry_msgs import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped
# from tf2_geometry_msgs import PointStamped

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
    ps.header.frame_id = "son1"
    ps.point.x = 1.0
    ps.point.y = 2.0
    ps.point.z = 3.0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #转换实现
        try:
            #计算son1相对于son2的坐标关系
            """ 
                参数1:目标坐标系
                参数2:源坐标系
                参数3:rospy.Time(0) --- 取时间间隔最近的两个坐标系帧(son1相对world与son2相对world)
                返回值:son1与son2的坐标系关系
             """
            ts = buffer.lookup_transform("son2","son1",rospy.Time(0))
            rospy.loginfo("父级坐标系:%s,子级坐标系：%s,偏移量(%.2f,%.2f,%.2f)",
                ts.header.frame_id,
                ts.child_frame_id,
                ts.transform.translation.x,
                ts.transform.translation.y,
                ts.transform.translation.z
                )
            ps_out = buffer.transform(ps,"son2")
                
            rospy.loginfo("转换后的坐标：(%.2f,%.2f,%.2f),参考的坐标系：%s",
                    ps_out.point.x,
                    ps_out.point.y,
                    ps_out.point.z,
                    ps_out.header.frame_id)
        except Exception as e:
            rospy.logwarn("错误提示：%s", e)
        rate.sleep()


