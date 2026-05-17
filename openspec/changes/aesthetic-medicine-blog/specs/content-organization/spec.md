## ADDED Requirements

### Requirement: 内容分类体系
系统 SHALL 支持 categories（手术类别）和 tags（项目标签）两种分类方式。

#### Scenario: 分类展示
- **WHEN** 用户访问 /categories/ 页面
- **THEN** SHALL 列出所有手术类别及其文章数量

#### Scenario: 标签展示
- **WHEN** 用户访问 /tags/ 页面
- **THEN** SHALL 以标签云或列表形式展示所有标签

#### Scenario: 分类过滤
- **WHEN** 用户点击某个分类链接
- **THEN** SHALL 显示该分类下的所有文章列表

### Requirement: 导航系统
站点 SHALL 提供清晰的主导航、面包屑导航和分页导航。

#### Scenario: 主导航
- **WHEN** 用户浏览任何页面
- **THEN** SHALL 在 header 区域显示主导航菜单，包含首页、文章分类、关于等链接

#### Scenario: 面包屑导航
- **WHEN** 用户在非首页页面
- **THEN** SHALL 显示面包屑导航，标明当前位置路径

#### Scenario: 文章分页
- **WHEN** 列表页文章数超过页面展示上限
- **THEN** SHALL 显示分页控件，支持上一页/下一页跳转

### Requirement: 归档页面
系统 SHALL 提供按时间线排列的文章归档页面。

#### Scenario: 归档展示
- **WHEN** 用户访问 /archives/ 页面
- **THEN** SHALL 按年份分组展示所有文章标题和发布日期
