# 自动驾驶学习笔记

源仓库地址：https://github.com/ApolloAuto/apollo  
所有内容均翻译并整理自官方文档和源代码

## 已完成的内容

- [Apollo 5.5安装和编译过程中遇到的问题](./doc/install&compile_problem.md)
- [Apollo 5.5的软件整体架构](./doc/apollo_5.5_architecture.md)
- [部分数据结构定义整理（持续完善中）](./proto)
- [一些基础算法和概念（持续完善中）](./doc/fundamental_algorithm.md)
- [Coursera课程中用到的代码及运行结果](./code/coursera)

## 文档阅读

所有文档内容均存储在[doc](./doc/)文件夹下，直接打开阅读即可。

## 数据结构解析

Apollo的数据结构代码采用[ProtoBuf](https://github.com/protocolbuffers/protobuf)管理和生成，因此本项目在分析数据结构时，采用直接在`.proto`文件上做注释的方式，直接对源码做解析。学习时仅需直接打开`.proto`文件即可。

## 目录结构

```
.
│  README.md
├─code
│  └─coursera
│      └─Visual Perception for Self-Driving Cars
│  
├─doc
│      apollo_5.5_architecture.md
│      Autoware_architecture.md
│      fundamental_algorithm.md
│      install_and_compile_problem.md
│      
├─proto
│  ├─map    
│  ├─perception     
│  ├─planning          
│  └─prediction   
│            
└─res
    ├─apollo_5.5_architecture        

```
