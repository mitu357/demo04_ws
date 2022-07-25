#! /usr/bin/env python
import rospy
import rosbag
from std_msgs.msg import String
""" 
    需求:读取磁盘上的bag文件
    流程：
        1.导包
        2.初始化
        3.创建rosbag对象并打开文件流
        4.读数据
        5.关闭流
 """

if __name__ == '__main__':
    rospy.init_node("read_bag_p")
    bag = rosbag.Bag("hello_p.bag","r")
    msgs = bag.read_messages("/liaotian")
    for topic,msg,time in msgs:
        rospy.loginfo("话题%s,消息:%s,时间:%s",topic,msg.data,time)
    bag.close()
