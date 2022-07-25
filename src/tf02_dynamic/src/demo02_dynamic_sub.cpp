#include "ros/ros.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "geometry_msgs/PointStamped.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
/* 
    订阅方实现:订阅发布的坐标系相对关系，传入一个座标点，调用tf实现转换
    流程：
        1.包含头文件
        2.设置编码，节点初始化 NodeHandle(必须的)
        3.创建订阅对象----》订阅坐标系相对关系
        4.组织座标点数据
        5.转换算法，需要调用tf内置实现
        6.最后输出

 */
int main(int argc, char  *argv[])
{
    setlocale(LC_ALL, "");
    ros::init(argc, argv, "static_sub");
    ros::NodeHandle nh;
    //创建订阅对象
    //3—1.创建一个buffer缓存
    tf2_ros::Buffer buffer;
    //3-2在创建监听对象(监听对象可以将订阅的数据存入buffer)
    tf2_ros::TransformListener listener(buffer);
    geometry_msgs::PointStamped ps;
    //参考的坐标系
    ps.header.frame_id = "turtle1";
    //时间戳
    ps.header.stamp = ros::Time(0.0);
    ps.point.x = 2.0;
    ps.point.y = 3.0;
    ps.point.z = 5.0;
    //转换算法
    //添加休眠
    // ros::Duration(2).sleep();
    ros::Rate rate(10);
    while (ros::ok())
    {
        //核心代码实现  ----将ps转换成相对于base_link的座标点
        geometry_msgs::PointStamped ps_out;
        /* 
            调用了buffer的转换函数transform
            参数1：被转换的坐标点
            参数2：目标坐标系
            返回值：输出的坐标点

            ps1:调用时必须包含头文件 tf2_geometry_msgs/tf2_geometry_msgs.h
            ps2：运行时存在的问题，抛出一个异常base_link不存在
                原因：订阅数据是耗时操作，可能在调用transform转换函数时，坐标系的相对关系还没有订阅到，因此出现异常
                解决：
                    方案1：在调用转换函数前执行休眠
                    方案2：异常处理
         */
        try
        {
            /* code */
            ps_out = buffer.transform(ps,"world");
            ROS_INFO("转换后的坐标值：(%.2f,%.2f,%.2f),参考的坐标系:%s",
            ps_out.point.x,
            ps_out.point.y,
            ps_out.point.z,
            ps_out.header.frame_id.c_str());
            
        }
        catch(const std::exception& e)
        {
            // std::cerr << e.what() << '\n';
            ROS_INFO("异常消息：%s",e.what());
        }
        rate.sleep();
        ros::spinOnce();    
        
    }
    
    return 0;
}
