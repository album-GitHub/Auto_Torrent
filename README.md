# Auto_Torrent

依赖torf编写的自动制种工具，方便提高制种效率

# 功能与特色
- **支持多文件制种（一个文件一个种子）、文件夹制种**

- **支持自动从tracker服务器列表地址获取tracker**

- **设置了三种模式添加trackers:**
\
&ensp;**1.添加默认tracker与tracker服务器列表获取的tracker**\
&ensp;**2.仅添加默认tracker**\
&ensp;**3.仅添加tracker服务器列表获取的tracker**

- **支持自定义制种块大小**

- **设置好配置文件后可进行快速便捷的制种**

# 使用方法

1.下载这三个文件`Auto_Torrent.py、Auto_Torrent_config.ini、requirements.txt`并放至同一目录下
   第一次使用请切换至脚本所在目录使用命令pip install -r requirements.txt 安装所需依赖
  
2.使用文本编辑器修改`Auto_Torrent_config.ini`文件，设置好: 制种模式（重要）、默认添加的tracker、制种块大小、获取tracker服务器列表地址（可选）、种子文件保存的路径（可选）

# 运行
可以直接把需要制种的文件拖拽到脚本上直接运行，或者在命令行中执行： `Auto_Torrent.py '制种文件或文件夹路径'`
