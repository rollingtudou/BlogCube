# 🌟 BlogCube 🌟

## 📖 简介
这是一个基于Python Flask框架的轻量级博客系统开源项目。它提供了用户注册、登录、发布文章、编辑文章、搜索文章等一系列功能。

## 🚀 功能亮点
- **用户认证**：注册新用户，安全登录。
- **内容管理**：发表、编辑、删除文章。
- **全文搜索**：快速找到感兴趣的文章。
- **个人资料**：管理个人信息和查看发布的历史文章。

## 🛠️ 技术栈
- **编程语言**：Python 3.x
- **Web框架**：Flask
- **数据库**：SQLite
- **前端技术**：HTML5, CSS3, JavaScript

## 📦 安装指南
1. **克隆仓库**
   ```bash
   git clone https://github.com/rollingtudou/BlogCube.git
   ```

2. **安装依赖**
   ```bash
   cd 项目名
   pip install -r requirements.txt
   ```

3. **初始化数据库**
   ```bash
   python initialize_db.py
   ```

4. **运行应用**
   ```bash
   python app.py
   ```
   应用将会在 `http://127.0.0.1:5000/` 运行。

## 💡 使用说明
- 访问 `http://127.0.0.1:5000/` 可以看到首页。
- 注册一个新用户并登录后，你可以在个人资料页面发布和编辑文章。
- 使用搜索框可以查找特定的文章。

## 🤝 贡献指南
欢迎贡献！请遵循以下步骤：
1. Fork这个仓库。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`
3. 提交你的更改：`git commit -am 'Add some feature'`
4. 推送你的分支：`git push origin feature/your-feature-name`
5. 提交一个Pull Request

## 📄 许可证
该项目采用MIT许可证，详情请见 [LICENSE](LICENSE) 文件。

## 📧 联系方式
如果你有任何问题或建议，请通过以下方式联系我：
- Email: fengk677@gmail.com
- GitHub: [rollingtudou](https://github.com/rollingtudou)

---

## 🎨 设计与图标
本项目使用了以下开源图标库：
- [Font Awesome](https://fontawesome.com/) - 提供了一系列高质量的图标。

## 📈 数据库结构
数据库使用SQLite，主要包含以下表格：
- `users` - 存储用户信息。
- `articles` - 存储文章信息。

## 🛡️ 安全
本项目遵循最佳安全实践，包括但不限于：
- 使用HTTPS进行数据传输。
- 密码存储使用哈希加盐。
