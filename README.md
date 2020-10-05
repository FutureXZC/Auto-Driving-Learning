# Apollo 学习笔记

源仓库地址：https://github.com/ApolloAuto/apollo  
所有内容均翻译并整理自官方文档和源代码

## 已完成的内容

- [Apollo 5.5的软件整体架构](./doc/apollo_5.5_architecture.md)
- [部分数据结构定义整理](./proto)

## 贡献者需知

- 若读者希望对本文做出贡献，但由于此前主机上登录了公网的github或gitlab账号，导致与本项目的账号发生冲突，请在该项目下使用以下命令（用户名和密码为本域中的用户名和密码）：

```
git remote set-url origin https://用户名:密码@github.com/FutureXZC/Apollo-Learning
```

- 读者需在本地创建一个自己的分支，然后pull request，审核通过后即可完成合并

- 每次新增文件，都需要更新下方`目录结构`板块中的目录树。请使用tree命令生成目录树，push时请先删除临时存储目录树的文件

- 所有的commit都请**使用英文命名**

## 文档阅读

所有文档内容均存储在[doc](./doc/)文件夹下，直接打开阅读即可。

## 数据结构解析

Apollo的数据结构代码采用[ProtoBuf](https://github.com/protocolbuffers/protobuf)管理和生成，因此本项目在分析数据结构时，采用直接在`.proto`文件上做注释的方式，直接对源码做解析。学习时仅需直接打开`.proto`文件即可。

## 目录结构

```
.
│  README.md
│  
├─doc
│      apollo_5.5_architecture.md
│      Autoware_architecture.md
│      install&compile_problem.md
│      
├─proto
│  ├─map
│  ├─perception   
│  ├─planning      
│  └─prediction    
|
└─res
    ├─apollo_5.5_architecture  
    ├─autoware_architecture 
    └─install&compile_problem
```
