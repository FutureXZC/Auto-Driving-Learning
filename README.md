# Apollo 学习笔记

源仓库地址：https://github.com/ApolloAuto/apollo  
所有内容均翻译并整理自官方文档和源代码

## 已完成的内容

- [Apollo 5.5的软件整体架构](./doc/apollo_5.5_architecture.md)
- 部分数据结构定义整理

## 阅读需知

### 文档阅读

所有文档内容均存储在[doc](./doc/)文件夹下，直接打开阅读即可。

### 数据结构解析

Apollo的数据结构代码采用[ProtoBuf](https://github.com/protocolbuffers/protobuf)管理和生成，因此本项目在分析数据结构时，采用直接在`.proto`文件上做注释的方式，直接对源码做解析。学习时仅需直接打开`.proto`文件即可。

## 目录结构

```
.
│  README.md
│  tree.txt
│  
├─doc  # 笔记文档 
│      apollo_5.5_architecture.md
│      
├─proto  # 由ProtoBuf工具定义的数据结构，用于生成代码
│  └─perception
│          BUILD
│          ccrf_type_fusion_config.proto
│          dst_existence_fusion_config.proto
│          dst_type_fusion_config.proto
│          fused_classifier_config.proto
│          map_manager_config.proto
│          motion_service.proto
│          pbf_tracker_config.proto
│          perception_camera.proto
│          perception_config_schema.proto
│          perception_lane.proto
│          perception_obstacle.proto
│          perception_ultrasonic.proto
│          probabilistic_fusion_config.proto
│          roi_boundary_filter_config.proto
│          rt.proto
│          sensor_meta_schema.proto
│          tracker_config.proto
│          traffic_light_detection.proto
│          
└─res  # 笔记中引用的各种资源文件，例如图片
    └─apollo_5.5_architecture
            ...
```
