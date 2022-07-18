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

#### **7.6**

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

#### 7.7

**今日工作**

今天的主要工作主要聚焦在代码的编写上面。具体地——

* 重新组织和实现了一系列的函数，例如`search_sourcce`函数。配置了更加丰富的参数，以便更好地支持复用。例如`clean_mode`等，不同的函数之间耦合性降低了。同时，更好地将不同功能的模块化的封装。
* 实现了`remove_comment`函数。之所以实现这个函数，是因为昨天说的，在正式的处理之前，要先去掉注释，如果去掉注释以后不包含该配置项，则可以将该文件过滤掉。换句话说，我们真正处理的，确实是和该配置项相关的文件。
* 确定了处理逻辑。现在处理的思路是先获取到影响的block，即一个行号范围：
  * 对源码的Token进行遍历
  * 如果获取到某一个Token，则记录下行号
  * 当读取到一个endif，则记录下行号，以此作为一个范围

**明日工作**

* 尝试思路

#### 7.8 

**今日工作**

今天的方法围绕预处理工具的使用展开。具体地——

* 通过预处理，得到一个Token的生成器，通过对Token的遍历，可以获取到预处理阶段的每一个Token
* 这里的Token实际上PCPP封装好的一个类，可以提供下面的信息——
  * Token的值，即字符串字面值，该字段用来判断包含CONFIG变量
  * Token的类型，例如关键字、表达式等
  * Token所在的行，所在的列信息等

> 其实目前最关键的就是三点——
>
> * 获取行号
> * 判断是不是变量
> * 获取结构，以此得到一个影响的范围

这里的第三点是最困难的，也是这个方案相比之前的最大的优势，虽然不再像以前给出一个精准的DIFF，但是也一定程度上增加了鲁棒性。

**明日工作**

* 继续完成这部分代码的尝试，因为这里所涉及的编译理论知识比较多，所以要稍微慢一点

#### 7.11 

**今日工作**

今天主要完成两方面的工作。一方面是继续一遍参阅文档，一遍写代码。对于昨天的“关键的三点“实现了前两点。第三点稍微有点卡住。此外，还做了一部分的可视化的工作。作为一个上游脚本，我希望能够像一个库一样，为调用提供接口。对于一个终端脚本，产生一些可视化的结果（大部分是HTML和SVG）展示效果会比较好。这部分的大致效果如下：

这是借助于一个预处理的库提供的可视化的功能，不过需要一定的裁剪。

![效果](https://cpip.readthedocs.io/en/latest/_images/HTMLLinux_cpu.c_ITU_edit1.png)

**明日计划**

继续完善脚本，探索可视化。

#### 7.12

**今日工作**

今天主要的进展是调通了之前提到的可视化工具。具体地——

* 解决了之前的版本不兼容的问题。这部分主要是通过`deadsnake`添加一个`ppa`源来解决的

* 修改了原有程序中的一个BUG，主要来自于Python版本改动以后部分行为的变化，例如函数的删除和API的改名等等。

  这部分的效果，会直接通过微信发给老师，解压以后直接打开`index.html`即可。可以看一下效果。感觉还是很不错的。

**明日计划**

* 其实从本质上讲目前的可视化已经成功显示了影响的范围，达成了我们的目标，但是如果想要作为一个上游任务的话，还是需要更加结构化的结果。目前思路有一点卡住，准备参照库的实现来做自己的实现，实现功能的裁剪。

#### **7.13**

**今日工作**

今天的主要进展是一方面对之前给老师发的HTML生成代码进行裁剪。具体地

* 对生成的html的代码进行修改和裁剪。只对其中的条件编译部分进行保留，其他的部分则不展示即可。
* 对工具的源码进行解读，为修改定制做好基础。

**明日计划**

* 继续影响范围的结构化的代码进行实现

#### 7.14 

**今日工作**

今天主要学习了CPIPMAIN的代码处理方式，理解了如何使用CPIP得到代码的行数范围统计功能。可能还能得到更多的统计信息，类似于之前的HTML中的统计栏，但是感觉对我们来说意义不大。具体地——

* 学习了CPIP库处理代码的思路。一般来说，我们将编译的过程分为预处理、词法分析、语法分析、语言分析、中间代码生成等阶段。但是实际上编译的预处理阶段也会设计很多语法的分析。CPIP就是这样，例如基本的if-else-end就可以认为是一个基本的语法，要想得到基本的范围，就必须对语法进行识别。
* 完成了部分代码编写，但是还有BUG。

**明日计划**

* 完成代码的编写，周末大规模跑一下，看看效果。

#### 7.15

**今日工作**

今天的工作比较顺利，进展也比较多。具体地——

* 在脚本方面，能够统计得到影响的范围信息 ，彻底解决了之前的如下类的问题。当然这有一个前提，就是我们认为，不管后面跟的是`&&`还是 `||`, `#ifdef`到`#else`中间的内容，我们都认为是和`CONFIG_CC`相关的代码。

  ```c
  #ifdef defined(CONFIG_CC) && defined(FOO_BAR)
  ...
  #else
  ...
  #endif
  ```

  更进一步，为了实现上述的功能，我们的核心代码段如下——

  ```python
  myLex = PpLexer.PpLexer(sys.argv[1], myH)
  res = [x.lineNum  for x in myLex.ppTokens() if 'CONFIG_CC' in myLex.condState[1]]
  ```

  可以看到这里使用了一个预处理的语法分析器，这里主要是根据当前代码段的宏状态（即condState)是否包含`CONFIG_XX`。

* 优化了之前的注释删除功能。从使用预处理的方法过渡到了直接使用`C/C++`的正则替换的功能。更加高效。

* 尝试大规模跑了一下脚本，不过因为现在到了语法级别的分析，所耗费的时间更多了，服务器有一点顶不住。想办法解决ing...

**明日工作**

* 总的来讲，目前的技术上的难点都已经被攻克，后面主要是将这些方法进一步大规模验证实现并调试

* 除此以外，我还想对可视化的功能进一步优化，把所有的源文件都放到一个网页中，更加直观