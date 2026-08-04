import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: (
    <div className="flex items-center gap-2">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 70 70"
        width="24"
        height="24"
        className="shrink-0"
        aria-hidden="true"
      >
        <path
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M64.883 1.813 62.037 4.66c-14.91 14.91-39.083 14.91-53.992 0L5.198 1.813a2.394 2.394 0 0 0-3.385 3.385L4.66 8.045c14.91 14.91 14.91 39.083 0 53.992l-2.847 2.846a2.394 2.394 0 0 0 3.385 3.386l2.847-2.847c14.91-14.91 39.082-14.91 53.992 0l2.846 2.847a2.394 2.394 0 1 0 3.386-3.386l-2.847-2.846c-14.91-14.91-14.91-39.083 0-53.992l2.847-2.846a2.394 2.394 0 0 0-3.386-3.386Z"
        />
      </svg>
      <span className="text-base font-semibold">Kent's Lab</span>
    </div>
  ),
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Kent 的个人实验室，记录区块链、稳定币、EVM、AI 工具与长期思考。" />
      <meta property="og:title" content="Kent's Lab｜Kent 的个人实验室" />
      <meta property="og:description" content="保持好奇，持续实验。这里记录技术探索、项目实践、工作复盘与生活观察。" />
      <meta property="og:site_name" content="Kent's Lab" />
      <style>{`
        /* Custom table of contents styles */
        .nextra-toc [data-level="1"] {
          color: #000 !important;
          font-weight: 600 !important;
        }
        .nextra-toc [data-level="1"]:hover {
          color: #2563eb !important;
        }
        .dark .nextra-toc [data-level="1"] {
          color: #fff !important;
        }
        .dark .nextra-toc [data-level="1"]:hover {
          color: #60a5fa !important;
        }

        /* Sidebar navigation styles - only first level */
        .nextra-sidebar-container *,
        .nextra-sidebar * {
          font-weight: normal;
        }

        .nextra-sidebar-container [data-level="1"],
        .nextra-sidebar [data-level="1"] {
          font-weight: 700 !important;
        }

        .nextra-sidebar-container [data-level="2"],
        .nextra-sidebar-container [data-level="3"],
        .nextra-sidebar-container [data-level="4"],
        .nextra-sidebar [data-level="2"],
        .nextra-sidebar [data-level="3"],
        .nextra-sidebar [data-level="4"] {
          font-weight: normal !important;
        }

        .nextra-main {
          border-left: 1px solid #e5e7eb !important;
          margin-left: 1rem !important;
        }

        .dark .nextra-main {
          border-left-color: #374151 !important;
        }

        .nextra-container > div:first-child {
          border-left: 1px solid #e5e7eb;
        }

        .dark .nextra-container > div:first-child {
          border-left-color: #374151;
        }

        .nextra-sidebar-container {
          border-right: 1px solid #e5e7eb !important;
          margin-right: 1rem !important;
        }

        .dark .nextra-sidebar-container {
          border-right-color: #374151 !important;
        }

        .nextra-toc {
          position: relative;
          padding-left: 1rem !important;
          margin-left: 1rem !important;
        }

        .nextra-toc::before {
          display: none;
        }
      `}</style>
    </>
  ),
  navigation: {
    prev: true,
    next: true
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true
  },
  toc: {
    float: true,
    title: '此页内容'
  },
  footer: {
    content: (
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span>© 2026</span>
          </div>
        </div>
        <div className="text-sm text-gray-500">保持好奇，持续实验。</div>
        <div className="text-sm text-gray-500">
          <a
            href="https://beian.miit.gov.cn/"
            target="_blank"
            rel="noreferrer"
            className="hover:text-gray-700 dark:hover:text-gray-300"
          >
            京ICP备2026033906号-1
          </a>
        </div>
        <div className="text-sm text-gray-500">
          <a
            href="https://beian.mps.gov.cn/#/query/webSearch?code=11011402056242"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 hover:text-gray-700 dark:hover:text-gray-300"
          >
            <img
              src="/beian-icon.png"
              alt="公安备案图标"
              width="16"
              height="16"
              className="shrink-0"
            />
            <span>京公网安备11011402056242号</span>
          </a>
        </div>
      </div>
    )
  }
}

export default config
