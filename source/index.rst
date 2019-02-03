.. ocg-rule documentation master file, created by
   sphinx-quickstart on Wed Oct 10 20:09:40 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================
Welcome to ocg-rule's documentation!
====================================

前言
============

| 游戏王OCG规则繁杂，中文资料大都比较陈旧，\ `新大师完全规则书 <https://legacy.gitbook.com/book/warsier/new_master_rule/details>`__\ 部分内容仍不够详细，因此我整理出了这个网站，方便查阅。
| 由于内容较多，全部记住几乎是不可能的，我也记不住。只要碰到问题时知道在哪或要搜什么就行了。
| 对某些内容有疑问、发现内容没有及时更新或者有错误，都可以通过下方的\ 联系方式_\ 联系我。

| 本站\ **支持全站搜索**\ ，并且\ **支持电子书下载**\ 。
| 从ygomobile内跳转到这，下列方式下载不了电子书没反应的话，可以长按复制本站网址：https://ocg-rule.readthedocs.io，用手机浏览器进入，就可以正常下载了。

-  电脑版网页的搜索框在左侧边栏，点击侧边栏底部v:latest/v:master一行就能看到下载pdf/epub文档的选项，方便没有网络时查看。
-  手机版网页要先点击左上角，出现侧边栏和搜索框，再点击底部。

.. tip::

   | 由于文中基本不用问答来介绍，搜索时不要用“怎样”“如何”等词，应该直接搜关键词。
   | 例如，不要搜“连锁怎么处理”，可以搜“连锁处理”。
   | 本站涉及的主要是比较复杂的规则和调整，如果是不清楚怎么融合召唤等，这里找不到答案的基础问题，还是要看\ `新大师完全规则书 <https://legacy.gitbook.com/book/warsier/new_master_rule/details>`__\ 。

| 相对pdf来说，epub文档更适合手机阅读，推荐用多看阅读打开。这两种格式的文档在电脑上都可以用Edge浏览器（win10 1709以上）打开。
| pdf/epub文档只是下载时的网站内容，由于我一直在更新，推荐定期重新下载。

.. tip:: 想看更新记录？点击这里→\ `lucays/ocg-rule/commit <https://github.com/lucays/ocg-rule/commits/master>`__\ 。

| 本站使用的卡名和效果文本等基本上是NW论坛XYZ龙加农的翻译版本，在此表示感谢。
| 卡查建议直接使用\ `ygocore <http://ygocore.ys168.com/>`__\ /\ `ygomobile <https://www.taptap.com/app/37972>`__\ 等游戏软件的卡组编辑功能。
| 也可以用\ `ourocg在线卡查 <http://www.ourocg.cn/>`__\ ，注意要在首页最下方改成优先使用NW文本。
| 或者用\ **微信小程序-我们的OCG**\，同样要在\ **设置-翻译文本偏好**\ 中调整为优先使用NW文本。
| 微信小程序-游戏王查卡器只能设置译名为NW版本，效果文本无法设置，虽然添加新卡的速度更快，由于CNOCG版翻译和NW相差比较大，不建议在本站对照使用。

.. note:: 只是我没有精力配CN版翻译重写，这段话没有比较两种翻译孰优孰劣的意思。

| 文章中的例子后的日期如果是超链接，点击后可以进入官方卡片数据库的FAQ原文。若进入的是英文首页，在右上角选日语后会自动刷新进入FAQ页面。
| 没有日期的例子基本来自\ `遊戯王カードWiki <http://yugioh-wiki.net>`__\和我自己的邮件等。wiki没有数据库那样的单独faq页面，也不一定放在单卡或用语页面的底部，我在编写时就没有附上页面链接，后续也可能会慢慢补上。
| 尽管很多卡片描述相似甚至一模一样，它们的裁定也有可能不一样。这样的情况在文中会用\ **特别**\ 一词注明。当然，也许只是我不了解原因。总之以事务局的裁定为准。

联系方式
========

| 直接在文章底部评论即可。
| 也可以加入qq群：768881279
| 或发邮件至：\ lucahhai@gmail.com\ /\ lucahhai@foxmail.com

源代码
=======

| 这些文章用\ `restructureText <https://zh-sphinx-doc.readthedocs.io/en/latest/rest.html>`__\ 写就。
| 所有内容的代码见：\ `lucays/ocg-rule <https://github.com/lucays/ocg-rule>`__\ 。
| 网站界面主题的代码见：\ `lucays/sphinx-typlog-theme <https://github.com/lucays/sphinx-typlog-theme>`__\ 。
| readthedocs托管文档的步骤参考\ `使用ReadtheDocs托管文档 <https://www.xncoding.com/2017/01/22/fullstack/readthedoc.html>`__\ 和\ `sphinx文档 <http://www.sphinx-doc.org/en/master/>`__\ 。

目录
=======

.. toctree::
   :maxdepth: 3
   :glob:

   新大师规则变更点
   chapters/*
