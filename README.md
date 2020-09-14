# Apollo 软件架构

## 软件架构

![架构](/软件架构/Apollo_5_5_Architecture.png)

### Perception

![Perception](/软件架构/Perception.png)

&emsp;&emsp;Perception（感知模块）识别自动驾驶车辆周围的世界，包含两个重要的子模块:障碍检测和交通信号灯检测。

&emsp;&emsp;Apollo的Perception模块包含以下新特性：

- 支持VLS-128 Line LiDAR
- 通过多个摄像头检测障碍
- 先进的交通信号灯检测
- 可配置的传感器融合

&emsp;&emsp;Perception模块合并了5个摄像头(2个前摄像头, 2个分别在两边，1个在尾部)、2个雷达(一前一后)配合3个16线激光(两后一前）以及1个128线激光的性能，以此识别障碍和融合他们各自的追踪数据来获取一个追踪列表。障碍子模块识别、分类和追踪障碍。该子模块同样可以预测障碍的运动和位置信息(例如运动方向和速度)。而车道线，我们利用后处理车道解析像素以及计算车道相对于智能车的位置来构造车道线实例(如L0, L1, R0, R1, 等)。

### Prediction

![Prediction](/软件架构/Prediction.png)

&emsp;&emsp;Prediction基于Perception模块感知的障碍来预测未来的运动轨迹。

&emsp;&emsp;Prediction模块为所有感知到的障碍预测未来的运动轨迹。输出的预测信息封装了感知信息。Prediction 订阅了Localization模块、Planning模块和Perception模块感知障碍的信息

&emsp;&emsp;当收到Localization模块的信息以后，Prediction模块会更新它的内部状态。真实的Prediction模块会在收到Perception模块发送的障碍感知信息以后触发。

### Localization

![Localization](/软件架构/Localization.png)

&emsp;&emsp;Localization模块聚合各种数据来定位智能车，包含两种定位模式OnTimer和Multiple SensorFusion。  

&emsp;&emsp;第一种定位模式使用基于RTK的定时器回调函数OnTimer。另一种定位模式是多传感器融合的方法（MSF），使用一系列基于事件触发的回调函数。

### Routing

![Routing](/软件架构/Routing.png)

&emsp;&emsp;Routing模块需要路径的起点和终点来计算道路。通常起点就是智能车的当前位置。

### Planning

![Planning](/软件架构/Planning.png)

&emsp;&emsp;阿波罗3.5使用几个信息源来计算一个安全无碰撞的轨迹，所以Planning模块需要与其他所有模块进行交互。随着阿波罗的成熟和在不同道路情况下驾驶实例的训练，Planning模块已经演变成为一个更加模块化、场景特殊化和整体化的方法。在这种方法中,每个驾驶用例被视为不同的驾驶场景。这是有用的，由于它们都被视为单个驾驶场景，因此现在在特定场景中报告的问题可以在不影响其他场景的工作的情况下得到修复，而不是以前的版本中问题修复会影响其他驾驶用例。  

&emsp;&emsp;一开始，Planning模块获取Prediction的输出。因为预测输出包裹了原始感知的障碍物，所以Planning模块订阅交通灯检测输出而不是感知障碍物输出。  

&emsp;&emsp;然后，Planning模块获取Routing的输出。在某些情况下，如果当前行走的路线没有被严格遵循，Planning模块也可以通过发送一个路径规划请求来触发新的路径计算。

&emsp;&emsp;最后，Planning模块需要知道定位信息（定位：我在哪里）和近期的智能车的相关信息（底盘：我的状态是什么）。

### Control

![Control](/软件架构/Control.png)

&emsp;&emsp;Control以规划的轨迹为输入，生成控制命令传递给CAN总线。它有五个主要的数据接口：OnPad、OnMonitor、OnChassis、OnPlanning和OnLocalization。  

&emsp;&emsp;OnPad和OnMonitor是与基于PAD的人机界面和模拟的常规交互。

### CanBus

![CanBus](/软件架构/CanBus.png)

&emsp;&emsp;CanBus有两种数据接口。第一个是基于事件发布的回调函数OnControlCommand；第二个是接收到控制命令时触发d OnGuardianCommand。

### HMI

![HMI](/软件架构/HMI.png)

&emsp;&emsp;Apollo中的人机界面或DreamView是web应用程序，功能包括：  

- 用于可视化相关自动驾驶模块的当前输出，例如规划轨迹、车辆定位、底盘状态等
- 提供人机界面，供用户查看硬件状态、打开/关闭模块以及启动自主驾驶汽车
- 提供调试工具，以有效地跟踪模块问题，如PnC Monitor  

### Monitor

![Monitor](/软件架构/Monitor.png)

&emsp;&emsp;车辆所有模块的监控系统，包括硬件。Monitor模块接收来自不同模块的数据，并将其传递给HMI，以便驾驶员观察并确保所有模块均正常工作。如果某个模块或硬件发生故障，monitor模块会向Guardian模块发送警报，Guardian模块会决定需要采取哪些措施来防止崩溃。  

### Guardian

![Guardian](/软件架构/Guardian.png)

&emsp;&emsp;Guardian模块主要是一个行动中心，它根据Monitor模块发送的数据做出行动决定。Guardian模块有两个主要功能：  

- 所有模块工作正常时：Guardian模块保证控制流正常工作。控制信号被发送到CAN总线，效果与不经过Guandian一样。
- 模块碰撞由Guardian检测-如果Guardian检测到故障，它将阻止控制信号到达CAN总线并使车辆停止。有三种方法可以让Guardian决定如何停车，而要做到这一点，Guardian会求助于最终的Gatekeeper和超声波传感器：  
    - 如果超声波传感器运行良好，但没有检测到障碍物，Guardian将使汽车缓慢停止
    - 如果传感器没有响应，Guardian会紧急刹车，使汽车立即停止
    - 特殊情况：如果HMI通知驾驶员即将发生的碰撞，并且驾驶员在10秒钟内未进行干预，则Guardian将采用紧急制动使车辆立即停止

> 注: 
> 1. 在上述任何一种情况下，Guardian将始终停止车辆监控检测到任何模块或硬件故障
> 2. Monitor和Guardian是解耦的，以确保没有单点故障，并且通过模块化方法，可以在使用额外的操作来修改操作中心的同时，不影响监控系统的功能，因为Monitor模块也与HMI通信
