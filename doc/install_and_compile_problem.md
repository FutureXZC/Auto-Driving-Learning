# Apollo: 0 packages loaded problem
## 原因分析
在安装时，使用的源码来自`https://github.com/ApolloAuto/apollo-kernel/releases`仓库，使用该仓库的源码下载的docker镜像仅包含Apollo内核，未包含能够配合Bazel执行编译的相关插件，同时该版本的源码不提供Can卡支持，需要自己安装Can卡，适合直接在实际应用的硬件环境上安装或单纯做源码学习，不适合用作demo的学习。  
>  Bazel编译至少需要BUILD.bazel和WORKSPACE两个文件，详见 https://www.jianshu.com/p/3a4a2b5f46de ，Apollo内核的配置文件需要由某个程序生成Bazel编译的支持，即生成上述文件。
## 解决方案
下载源码时，使用来自`https://github.com/ApolloAuto/apollo`仓库的源码进行安装，该仓库的源码包含所有本地运行需要的一切基本支持，正确下载并按照官方的指导运行后能够正确执行编译。

# problem: Apollo compile ERROR

在进入到docker内部执行`./apollo.sh build`时，无法正常下载某些包依赖。如图所示，此处无法下载civetweb包，影响到后续的编译。  
此前在下载包ad-rss-lib时，也出现过类似的问题。
![error](/res/install_and_compile_problem/0_package_error.png)

## 写在前面

请先明确自己下载的Apollo源码版本，如果是master分支的（`apollo`文件夹下**没有**`WORKSPACE.in`），可以继续阅读，网络上没有其他任何一篇博客的方案比本文有效；如果是其他版本（`apollo`文件夹下**有**`WORKSPACE.in`），请直接借鉴 https://blog.csdn.net/Lo_Bamboo/article/details/105214674 ，继续阅读本文对你解决问题毫无借鉴意义。  

## 原因分析

阅读上述问题的报错信息可知，是在从`https://github.com/civetweb/civetweb/archive/v1.11.tar.gz`处下载包失败。由于被微软收购后，github的服务器几乎全在美国，物理距离较远，加之“万里长城”的阻拦，使得国内用户常常因网络原因难以正常下载github上的资源。docker容器借用的也是host的网络，因此在docker容器内部下载同样会十分缓慢。“科学上网”可以一定程度缓解网速过慢的问题，但也是杯水车薪。一旦clone的过程中由于网速过慢或短期无响应被git判定为断线，就会导致下载失败。  
  
找到报错信息中的路径，可以看到在`.cache`目录下包含的就是所有编译过程中的缓存，而第三方包均在`external`中，如下图所示。所有成功编译的包，都会生成对应的.marker文件，而原题中编译失败的civetweb包仅会存在一个没有完整文件的文件夹，没有生成对应的marker文件。  
  
原问题中提到的ad-rss-lib包问题，多次尝试后下成了，纯属运气好。网络一通畅就下成了...所以其实这个下载对欧皇友好...  
  
另外，linux下的git具有断点续传的功能，这一点比windows系统下的git要好（随便找个几G的大项目试试，必断线，然后可以在目标位置发现一个下了一半的项目文件/文件夹）。尽管容器内挂载的系统也是linux，但是一旦被判定为断线而下载失败，就会终止编译程序，下次编译时由于检测不到包对应的.marker文件，又会重新下载，所以在该编译环境下实则是失去了断点续传的功能。  
  
![cache](/res/install_and_compile_problem/cache.jpg)  

## 解决方案

我们利用断点续传的机制，在host下直接访问下载失败的资源仓库，（可能需要多次重连）就可以得到完整的包。然后在编译配置文件中修改获取包的地址（**注意**：不同版本的配置文件位置不同！），即将原本应在线获取的包改为本地获取，即可完成包的加载，正确执行后续的编译。下面以civetweb包为例做详细解释。

### 包下载

在host下`git clone https://github.com/civetweb/civetweb/archive/v1.11.tar.gz`即可下载，如果断线就重复执行该命令，直至完整下载整个包。

### 将包放入数据卷内

docker具有数据卷机制，能够实现容器和host之间共享文件和文件夹。而Apollo项目的共享文件夹就是`apollo`（也可能叫做`apollo-5.0`、`apollo-master`或者其他什么名字，取决于clone源码时的仓库和分支名字，为便于描述，本文中的`apollo`文件夹即表示共享文件夹），将下载好的包直接放入`apollo`文件夹下即可在容器内被检测到。如下图，我将包文件夹命名为`civetweb-1.11`：  
  
![save-place](/res/install_and_compile_problem/save-place.jpg)  

>  Docker容器数据卷详解（共享数据）：https://blog.csdn.net/weixin_40322495/article/details/84957433

### 修改包对应的配置文件

由于docker的数据卷机制，以下所有操作均可以在host下完成。  
  
Apollo项目中所有第三方包的配置数据均在`third_party`中，该目录下的所有文件夹中都至少拥有`包名.BUILD`、`BUILD`和`workspace.bzl`三个文件，他们共同构成了Bazel编译所需的一切配置。在`workspace.bzl`中配置的就是包的安装位置。在容器中含有一些基本的库支持，因此某些包的配置只需要写入本地加载的信息即可，例如如下图所示的adolc包的配置信息，其path指向的是容器内挂载系统的`/usr/include`。**注意**：该路径是容器内的绝对路径，而非host的，容器内部也是一个linux系统，除`apollo`外该系统下的其他目录都没有挂载到数据卷上。  
  
![local-config](/res/install_and_compile_problem/local-config.jpg)  
  
因此，我们只需要找到安装出错的civetweb包的配置文件，并模仿adolc这样本地加载的包的配置文件进行书写即可，即包裹在native.new_local_respository内，如下图所示：  
  
![myconfig](/res/install_and_compile_problem/myconfig.jpg)  
  
在我的host中，包文件夹实际上在`/home/xiang/apollo/civetweb-1.11`下，但是可以看到，我的路径配置并不是这样写的。由于编译是在容器中执行的，而在容器中，`apollo`文件夹就在根目录下，所以这里的路径实际上写的是在容器中的绝对路径，即`/apollo/civetweb-1.11`。注意，这里的build_file参数要记得做对应的修改，name应该填上包名。  
  
我注释掉的http_archive部分即为该包原本的配置信息。一看该函数的名字就知道这是一个远程获取包的配置。repo函数下包裹的两种获取方式对应的参数介绍如下：

*  name：包名，显然
*  build_file：待编译文件，导向的就是第三方包的位置下的BUILD文件，即本目录下的BUILD文件
*  sha256：校验和，类似于MD5码（或者说他就是MD5？我不明确），用于核对在线下载的包是否是本程序真正需要的包，防止用了被篡改的包而产生隐患
*  strip_prefix：预处理文件名，下载下来的包通常是一个tar.gz文件或者一个文件夹，需要指定文件名或者文件夹名以进行预处理（例如解压、拷贝什么的）
*  urls：下载的地址，显然
*  path：本地来源路径，必须写在容器内的绝对路径

在最新版的Apollo项目中，所有经过在线下载的包都需要核对校验和sha256，因此，如果尝试修改urls以使用码云或其他国内镜像下载，会产生校验和出错的问题。报错信息中可以看到镜像文件的校验和，我们可以复制报错信息中的sha256在配置文件内进行修改，但是下次编译时，下载的校验和又会不同，这可能跟码云或某些国内镜像站生成校验和的方式有关（对同一个文件来讲MD5不会变，因此从这点看这个sha256应该不是MD5？）。**在master版本中修改镜像urls和sha256已被为证明是徒劳，没有必要重新踩坑。**  
  
**使用非master分支下的源码进行安装的选手请注意**：配置信息修改可以参考本篇博客： https://blog.csdn.net/Lo_Bamboo/article/details/105214674 ，其配置文件对应的位置是`/apollo/WORKSPACE.in`。在这些版本中，可以直接修改下载地址，而编译时程序不会检查校验和，所以可以有修改镜像地址进行下载以及本地加载两种解决方案。而**master分支下仅支持本地加载**！

### 执行编译

修改完上述配置后，进入容器编译即可。编译结束后可以看到生成了几个`bazel-×`文件，如下图。此时就可以正确运行Apollo项目了。  
  
![compile-res](/res/install_and_compile_problem/compile-res.jpg)