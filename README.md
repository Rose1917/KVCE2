# Kernel Variable Code Exactor(KVCE) 

#### 🔗快速跳转

- 🚀[最新进展](#71)
- 🎉[任务描述](#1-任务描述)
- 🎈[最终产物](#2-最终产物)

#### 1. 任务描述

* 主线任务：编写一个脚本，该脚本能够：
  1. 根据任一内核源代码（任务以内核`5.15.9`为例），得到所有的内核配置项。
  2. 对于任意一个配置项，能够定位到它所对应和影响的文件、文件中的代码片段等分析报告
* 支线任务：
  1. 根据任一内核源代码的补丁，得到该补丁的所有的文件
  2. 根据该补丁影响的所有文件，推测出该补丁版本影响的所有的内核配置项
  3. 对该补丁的相关的配置项，得到相关的文件、代码片段等分析报告

#### 2. 最终产物

最终的项目交付，是以一个`Repo`的形式，最终的`Repo`中应该包含如下的内容：

* 任务描述中的脚本文件

* 示例内核源代码（以内核`5.15.9`为例）

* 输出的Json文件：

  ```json
  config_name:{
      release_time: XXXX-XX-XX
      file_name1:{
          func_name1: 
     {
      start_line,
      end_line
     }
          func_name2:
     {
      start_line,
      end_line
     }  
          ....
          func_nameN: 
     {
      start_line,
      end_line
     }
      } 
  
      ...
  
      file_nameN:{
          func_name1:    
     {
      start_line,
      end_line
     }
          func_name2: 
     {
      start_line,
      end_line
     }
          ....
          func_nameN:    
     {
      start_line,
      end_line
     }
      }  
  }   
  ```

  

* 针对git 补丁的json :

  ```json
  config_name:{
      git_id1:{
          op_status:XXX  // create, update, del 
          op_time: XXXX-XX-XX
          file_name1:{
              func_name1: {add:xx,del:xx}
              func_name2: {add:xx,del:xx}
              ....
              func_nameN: {add:xx,del:xx}
          }  
             
          ....
          
          file_nameN:{
              func_name1: {add:xx,del:xx}
              func_name2: {add:xx,del:xx}
              ....
              func_nameN: {add:xx,del:xx}
          }     
      }
  
      ...
  
      git_id2:{
          op_status:XXX  // add, update, del 
          op_time: XXXX-XX-XX
          file_name1:{
              func_name1: {add:xx,del:xx}
              func_name2: {add:xx,del:xx}
              ....
              func_nameN: {add:xx,del:xx}
          }  
             
          ....
          
          file_nameN:{
              func_name1: {add:xx,del:xx}
              func_name2: {add:xx,del:xx}
              ....
              func_nameN: {add:xx,del:xx}
          }     
      } 
  }
  ```

  

### Appendix A: Daily Work

---

#### 7.1 

**工作内容**

今天的工作主要是新建了一个Repo，并且细化了我的下一步的工作计划。

* 新的Repo地址，是`https://github.com/Rose1917/KVCE2`. 之前的`Repo`因为是和侯博老师主要对接的，内容后续管理也比较杂乱，所以就使用新的`Repo`。这个`Repo`主要有以下几个功能——
  * 汇报我的进度，使用文档的方式汇报进度会更加地有条理
  * 作为代码的文档，后续会有更多的部分加入进来，来对代码进行说明

* 制定了下一步的工作计划，具体地——
  * 把代码整理成一个`python`库的形式，其他人只需要进行`import`就可以
  * 对其他格式的文件进行处理
  * 对源代码文件进行更细致的处理，例如获取行号、获取函数名等

* 将之前的提取内核变量的代码结果，修改成了`json`的输出格式，方便下一步的处理

**明日工作**

* 整理代码，上传Github

#### 7.4

**工作内容**

今天的工作主要是对之前的代码进行了重构。具体地——

* 将之前的bash/python混用的代码重新使用python进行了重写，所有的代码都在`kvce.py`中
* 将之前的函数进行了更好的封装，更容易被其他的库和代码进行调用
* 对相关文件的格式进行检测——这部分的内容请参照函数`decide_extend`
* 对代码添加了更多的文档和注释

这部分的代码已经上传。

**明日工作**

* 对文件格式检测函数进行调整，使其能够`cover`更多的格式
* 对复杂的宏表达式类型想办法处理，给出一个合理的`report`

