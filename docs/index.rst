.. ocg-rule documentation master file, created by
   sphinx-quickstart on Wed Oct 10 20:09:40 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================
Welcome to ocg-rule's documentation!
====================================

.. role:: strike
    :class: strike

前言
======

| 游戏王OCG规则繁杂，中文资料大都比较陈旧，\ `新大师完全规则书 <https://legacy.gitbook.com/book/warsier/new_master_rule/details>`__\ 部分内容仍不够详细，因此我整理出了这个网站，方便查阅。
| 由于内容较多，全部记住几乎是不可能的，我也记不住。只要碰到问题时知道在哪或要搜什么就行了。
| 这个页面有本站的使用方法和注意事项，我的\ 联系方式_\ ，本站详细\ 目录_\ 和\ 部分文章介绍_\ ，请阅读了解后再查看其他内容，不要直接跳过。
| 对某些内容有疑问、发现内容没有及时更新或者有错误，都可以通过下方的\ 联系方式_\ 联系我。

| 本站\ **支持全站搜索**\ ，并且\ **支持电子书下载**\ 。
| 从ygomobile内跳转到这，下列方式下载不了电子书没反应的话，可以长按复制本站网址：https://ocg-rule.readthedocs.io，用手机浏览器进入，就可以正常下载了。

-  电脑版网页的搜索框在左侧边栏，点击侧边栏底部v:latest/v:master一行就能看到下载pdf/epub文档的选项，方便没有网络时查看。
-  手机版网页要先点击左上角，出现侧边栏，再点击底部找到下载选项。

.. tip::

   | 由于基本不用问答方式介绍，搜索时应该直接搜关键词。例如，应当搜『伤害步骤』，不要搜『:strike:`伤害步骤是什么`』。
   | 如果只想看\ **精确匹配**\ 的搜索结果，需要在搜索词前后加上英文双引号。假如搜索词是『这个回合』，应该输入『"这个回合"』。
   | 卡名基本用来举例，因此搜卡名不一定有结果。部分字段原文是英文的不会翻译。例如，「E·HERO 天空侠」可以搜「天空侠」，不要搜「:strike:`元素英雄`」。
   | 一些英文简称也不会翻译。例如，S·X·P对应同调·XYZ·灵摆，除了「同调解除」这样，卡名包含后者等情况，不会使用后者，不要搜『:strike:`同调·XYZ·灵摆`』。
   | 本站涉及的主要是疑难的规则和调整，如果是不清楚怎么召唤怪兽等，这里找不到答案的基础问题，还是要看\ `新大师完全规则书 <https://legacy.gitbook.com/book/warsier/new_master_rule/details>`__\ 。

| pdf目前部分文字显示存在问题，epub没有这些问题，并且对文本重新排版了，更适合手机阅读。
| 阅读器的话，手机上推荐多看阅读app（需下载安装），电脑上直接用windows10内置的Edge浏览器即可（无需下载软件）。
| pdf/epub文档只是下载时的网站内容，由于网站内容一直在更新，推荐定期重新下载。

.. tip:: 想看更新记录？点击这里→\ `lucays/ocg-rule/commit <https://github.com/lucays/ocg-rule/commits/master>`__\ 。

| 本站使用的卡名和效果文本等基本上是NW论坛XYZ龙加农的翻译版本，在此表示感谢。
| 卡查建议直接使用\ `ygocore <http://ygocore.ys168.com/>`__\ /\ `ygomobile <https://www.taptap.com/app/37972>`__\ 等游戏软件的卡组编辑功能。
| 也可以用\ `ourocg在线卡查 <http://www.ourocg.cn/>`__\ ，注意要在首页最下方改成优先使用NW文本。
| 或者用\ **微信小程序-我们的OCG**\，同样要在\ **设置-翻译文本偏好**\ 中调整为优先使用NW文本。
| 微信小程序-游戏王查卡器只能设置译名为NW版本，效果文本无法设置，虽然添加新卡的速度更快，由于CNOCG版翻译和NW相差比较大，不建议在本站对照使用。

.. note:: 只是我没有精力配CN版翻译重写，这段话没有比较两种翻译孰优孰劣的意思。

| 文章中的例子后的日期如果是超链接，点击后可以进入官方卡片数据库的FAQ原文。若进入的是英文首页，在右上角选日语后会自动刷新进入FAQ页面。
| 没有日期的例子基本来自\ `遊戯王カードWiki <http://yugioh-wiki.net>`__\和玩家们（不止我）的邮件等。
| 尽管很多卡片描述相似甚至一模一样，它们的裁定也有可能不一样。这样的情况在文中会用\ **特别**\ 一词注明。当然，也许只是我不了解原因。总之以事务局的裁定为准。

其他贡献者
===========

感谢下列玩家给这些文章提供了部分邮件调整，或纠正了一些不规范或错误的地方（或两者都有）：

- 小红帽
- 罗伽
- 圆环之理
- Yuzuha
- 日常的夏娜
- 苍蓝
- 青眼波涛

部分文章介绍
==============

部分文章的标题不容易看出介绍了什么，下面是主要内容解释。

| 不懂新大师规则？→\ :ref:`新大师规则变更点`\。
| 想知道事务局最近调整了哪些卡的规则？→\ :ref:`2019`\。
| 对时点、取对象这些基础概念不熟悉？→\ :ref:`基本用语`\。
| 「灰流丽」和「星尘龙」有什么区别？→\ :ref:`效果处理的不确定性`\。
| 为什么特殊召唤后不能发动「强欲而谦虚之壶」，发动过其他魔法·陷阱效果还能再发动「雪花之光」？→\ :ref:`誓约`\。
| 错过时点是什么，手卡诱发有什么特点，非公开情报要注意什么，多个效果同时满足条件该怎么排序？→\ :ref:`诱发类效果`\。

联系方式
========

| 直接在文章底部评论即可。
| 也可以加入qq群：768881279
| 或发邮件至：\ lucahhai@gmail.com\ /\ lucahhai@foxmail.com

目录
=======

.. toctree::
   :maxdepth: 3
   :glob:

   新大师规则变更点
   chapters/*

源代码
=======

| 这些文章用\ `restructureText <https://zh-sphinx-doc.readthedocs.io/en/latest/rest.html>`__\ 写就。
| 所有内容的代码见：\ `lucays/ocg-rule <https://github.com/lucays/ocg-rule>`__\ 。
| 网站界面主题的代码见：\ `lucays/sphinx-typlog-theme <https://github.com/lucays/sphinx-typlog-theme>`__\ 。
| readthedocs托管文档的步骤参考\ `使用ReadtheDocs托管文档 <https://www.xncoding.com/2017/01/22/fullstack/readthedoc.html>`__\ 和\ `sphinx文档 <http://www.sphinx-doc.org/en/master/>`__\ 。

广告相关
==========

| 本项目托管在\ `readthedocs <https://readthedocs.org/>`__\ ，一个可以免费发布文档的网站。
| 以前，readthedocs只会给使用官方主题的项目网页加上广告，只要使用自己编写的第三方主题（例如本网站），就不会有广告。
| 不过，readthedocs公告宣布现在会给所有项目加上广告：\ `New Ad Format Coming to Read the Docs Community Sites <https://blog.readthedocs.com/fixed-footer-ad-all-themes/>`__\。
| 请注意这些广告与我没有任何关系，我也无法再去除。
