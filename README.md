# 基于Web的互联网广告平台

## 重要链接

### 需求分析&设计：
https://sawp25tdzaj.feishu.cn/docx/LHw8dCZm4ovnl4xgOplcMhMOn2g?from=from_copylink 

### 进度（实时更新）：  
https://sawp25tdzaj.feishu.cn/docx/YdEMdKTBpoGUc9xfnK1cjaBjnpd?from=from_copylink 


## 快速上传代码到 GitHub 仓库流程

👉 仓库地址是：[https://github.com/carolynwei/ads_platform](https://github.com/carolynwei/ads_platform)

步骤如下：

### 第一步：克隆（下载）仓库到本地
在自己的电脑终端/命令行执行：

```bash
git clone https://github.com/carolynwei/ads_platform.git
```

这样大家都有一份一模一样的项目。

然后进入项目文件夹：

```bash
cd ads_platform
```

---

### 第二步：新建自己的分支
为了避免大家直接改 `main` 分支，**每个人要新建自己的分支**。  
比如张三要开发登录功能，可以新建一个 `feature-login` 分支：

```bash
git checkout -b feature-login
```

---

### 第三步：在自己的分支上写代码
直接在 `feature-login` 分支上写代码、改文件。

改完之后，执行：

```bash
git add .
git commit -m "feat: 完成了登录功能"
```

**`add`** 是告诉 Git 哪些改动要提交，  
**`commit`** 是记录一次提交。

---

### 第四步：推送自己的分支到 GitHub
推送你的分支到远程：

```bash
git push origin feature-login
```

推送成功后，GitHub 上就能看到这个分支了！

---

### 第五步：在 GitHub 上发起 Pull Request
1. 打开仓库：[https://github.com/carolynwei/ads_platform](https://github.com/carolynwei/ads_platform)
2. 会看到提示 `Compare & pull request`，点进去。
3. 填写一下标题，比如【完成登录功能】，然后点【Create pull request】。
4. 让负责人 review（审核），通过之后合并到 `main`。

---

### 小提醒 ✨
- 每次开发新的功能，建议都建一个新的分支，不要直接在 main 上改。
- 提交信息要尽量规范，比如 `feat: 完成注册功能`，`fix: 修复登录bug` 这样。
- 写完功能及时发 PR，不要拖太久！

---
