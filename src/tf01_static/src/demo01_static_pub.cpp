#include "ros/ros.h"
#include "tf2_ros/static_transform_broadcaster.h"
#include "geometry_msgs/TransformStamped.h"
#include "tf2/LinearMath/Quaternion.h"
/* 
    需求：发布两个坐标系之间的相对关系

    流程：
        1.包含的头文件
        2.设置编码 初始化ros节点 NodeHandle
        3.创建发布对象
        4.组织被发布的消息
        5.发布数据
        6。spin()

 */
int main(int argc, char *argv[])
{
    setlocale(LC_ALL, "");
    ros::init(argc, argv, "static_pub");
    ros::NodeHandle nh;
    tf2_ros::StaticTransformBroadcaster pub;
    geometry_msgs::TransformStamped tfs;
    tfs.header.stamp = ros::Time::now();
    tfs.header.frame_id = "base_link";//相对坐标系关系中被参考的那个
    tfs.child_frame_id = "laser";
    tfs.transform.translation.x = 0.2;
    tfs.transform.translation.y = 0.0;
    tfs.transform.translation.z = 0.5;
    //需要根据欧拉角转换
    tf2::Quaternion qtn;//创建四元数对象
    //向该对象设置欧拉表，这个对象可以将欧拉角转换成四元数
    qtn.setRPY(0,0,0);//欧拉角的单位是弧度
    tfs.transform.rotation.x=qtn.getX();
    tfs.transform.rotation.y=qtn.getY();
    tfs.transform.rotation.z=qtn.getZ();
    tfs.transform.rotation.w=qtn.getW();
    pub.sendTransform(tfs);
    ros::spin();
    return 0;
}
