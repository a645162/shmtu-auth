import { defineConfig } from 'vitepress'

function resolveBase() {
  const repo = process.env.GITHUB_REPOSITORY?.split('/')[1]
  if (!process.env.GITHUB_ACTIONS || !repo) {
    return '/'
  }
  return repo.endsWith('.github.io') ? '/' : `/${repo}/`
}

export default defineConfig({
  base: resolveBase(),
  lang: 'zh-CN',
  title: 'shmtu-auth 校园网自动认证',
  description: '上海海事大学校园网自动认证工具 — CLI / GUI / Docker 全平台支持',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: '概览', link: '/' },
      { text: '安装', link: '/install/' },
      { text: '认证流程', link: '/auth/dual-login' },
      { text: 'API', link: '/api/' },
      { text: 'Docker', link: '/docker/headless' },
    ],
    sidebar: [
      {
        text: '概览',
        items: [
          { text: '文档首页', link: '/' },
          { text: '快速开始', link: '/getting-started' },
          { text: '安装指南', link: '/install/' },
          { text: '项目结构', link: '/project-structure' },
        ],
      },
      {
        text: '认证流程',
        items: [
          { text: '双策略登录', link: '/auth/dual-login' },
          { text: '网络检测', link: '/auth/network-check' },
          { text: '监控循环', link: '/auth/monitor-loop' },
        ],
      },
      {
        text: '配置',
        items: [
          { text: '环境变量', link: '/config/env-vars' },
          { text: 'TOML 配置文件', link: '/config/toml' },
          { text: '配置优先级', link: '/config/priority' },
        ],
      },
      {
        text: 'Docker 部署',
        items: [
          { text: 'Headless 版本', link: '/docker/headless' },
          { text: '完整版镜像', link: '/docker/full' },
        ],
      },
      {
        text: 'GUI',
        items: [
          { text: 'GUI 用户指南', link: '/gui/overview' },
          { text: '系统托盘', link: '/gui/system-tray' },
        ],
      },
      {
        text: 'API',
        items: [
          { text: '核心 API', link: '/api/' },
        ],
      },
      {
        text: '开发',
        items: [
          { text: '开发环境搭建', link: '/dev/setup' },
          { text: '构建与打包', link: '/dev/build' },
        ],
      },
      {
        text: '附录',
        items: [
          { text: '故障排除', link: '/faq' },
        ],
      },
    ],
    outline: [2, 3],
    search: {
      provider: 'local',
    },
    footer: {
      message: 'shmtu-auth Docs',
      copyright: 'Copyright © shmtu-auth',
    },
  },
})
