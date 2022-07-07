# Kernel Variable Code Exactor(KVCE) 

#### 🔗快速跳转

- 🚀[最新进展](#74)
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

#### 7.5 

**工作内容**

今天的工作主要是对文件格式匹配函数做了一些调整，以及学习了一些更高级的C语言处理工具PCPP。

具体地——

* 之前在对文件格式进行匹配的时候，对于格式未知的文件统一进行统计到`unmatched_files`中，这样不方便后续的处理和量化估计（例如评价我们的工作到底`cover`掉了多少的文件）。现在使用`others`分类将这些文件都放进去。
* PCPP是一个功能更加强大、也更加丰富的C语言处理Python工具包。提供了例如`preprocessor`和`evaluator`等的工具。学习了该工具的基本使用，为提供更高级的分析结果打好基础。

**明日工作**

* 继续学习PCPP探索将PCPP利用起来的方法。

**7.6**

**工作内容**

今天主要是进行了进一步的调研和尝试。具体来说——

* 复现了之前的表达式宏的问题（侯博老师在群里发过）。具体来说，假如有一个宏表达式如下

  ```c
  #ifdef CONFIG_CC_IS_GCC && CONFIG_FOO_BAR
  void function_XXX()
  #endif
  ```

  那么我们只单纯地通过打开和关闭宏`CONFIG_CC_IS_GCC`分别处理，然后做`diff`进行比较，是无法解决这个问题的，因为这个表达式还依赖于`CONFIG_FOO_BAR`。但是这个问题如果想要得到较好的解决，不能依赖这种方法。考虑一个极端的例子：

  ```c
  #ifdef CONFIG_CC_IS_GCC && (CONFIG_FOO && !CONFIG_BAR)
  void function_XXX()
  #endif
  ```

  

  所以为了更好地解决这个问题，需要换一个思路。实际上本质上来说，我们也不需要一个`diff`。我们关注的是——如何影响这份源文件的。如果我们能知道它所在的结构其实也是可以的。但是因为这些过程仍然是发生在预处理阶段的，所以我们仍然需要关注预处理器。

* CPIP和PCPP都是一个使用Python实现的预处理器，我们之前使用的是PCPP。因为只需要一些粗粒度的处理结果。但是CPIP则是Token级别对用户可见。所以为了得到更高精度的结果，可以使用CPIP。
* CPIP还提供了部分的可视化功能，后面如果能利用起来的话，工作会更加丰富。

**明日计划**

* 注释删除功能实现。为什么要单独实现一个注释删除，因为过滤掉注释以后，我们就可以更加专注于处理。
* 继续学习CPIP的Plexer.