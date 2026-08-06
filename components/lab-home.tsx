import { useEffect, useRef } from 'react'
import styles from './lab-home.module.css'

const links = [
  {
    href: '/life/',
    index: '01',
    title: '生活随笔',
    note: 'LIFE / MOMENTS'
  },
  {
    href: '/tech/',
    index: '02',
    title: '技术笔记',
    note: 'BUILD / RESEARCH'
  },
  {
    href: '/work/',
    index: '03',
    title: '工作札记',
    note: 'NOTES / REVIEW'
  },
  {
    href: '/about/',
    index: '04',
    title: '关于 Kent',
    note: 'PROFILE / CONTACT'
  }
]

export default function LabHome() {
  const shellRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)')
    const svg = shellRef.current?.querySelector('svg')
    const syncMotion = () => media.matches ? svg?.pauseAnimations() : svg?.unpauseAnimations()

    syncMotion()
    media.addEventListener('change', syncMotion)
    return () => media.removeEventListener('change', syncMotion)
  }, [])

  function handlePointerMove(event: React.PointerEvent<HTMLElement>) {
    const shell = shellRef.current
    if (!shell || event.pointerType === 'touch') return

    const bounds = shell.getBoundingClientRect()
    const x = (event.clientX - bounds.left) / bounds.width - 0.5
    const y = (event.clientY - bounds.top) / bounds.height - 0.5

    shell.style.setProperty('--eye-x', `${x * 9}px`)
    shell.style.setProperty('--eye-y', `${y * 6}px`)
    shell.style.setProperty('--core-x', `${x * 5}px`)
    shell.style.setProperty('--core-y', `${y * 4}px`)
  }

  function resetPointer() {
    const shell = shellRef.current
    if (!shell) return
    shell.style.setProperty('--eye-x', '0px')
    shell.style.setProperty('--eye-y', '0px')
    shell.style.setProperty('--core-x', '0px')
    shell.style.setProperty('--core-y', '0px')
  }

  return (
    <section
      ref={shellRef}
      id="kent-lab-home"
      className={styles.shell}
      onPointerMove={handlePointerMove}
      onPointerLeave={resetPointer}
      aria-labelledby="lab-home-title"
    >
      <div className={styles.paperNoise} aria-hidden="true" />

      <nav className={styles.dock} aria-label="实验室入口">
        {links.map(link => (
          <a href={link.href} className={styles.dockItem} key={link.href}>
            <span className={styles.dockIndex}>{link.index}</span>
            <span className={styles.dockTitle}>{link.title}</span>
            <span className={styles.dockNote}>{link.note}</span>
            <span className={styles.arrow} aria-hidden="true">↗</span>
          </a>
        ))}
      </nav>

      <header className={styles.intro}>
        <p className={styles.eyebrow}>
          <span>PERSONAL R&amp;D SPACE</span>
          <span className={styles.status}><i /> LAB ONLINE</span>
        </p>
        <h1 id="lab-home-title">Kent&apos;s Lab</h1>
        <p className={styles.lead}>保持好奇，持续实验。</p>
        <a className={styles.labEntry} href="/life/">
          <span className={styles.entryEyes} aria-hidden="true">
            <span className={styles.eye}><i /></span>
            <span className={styles.eye}><i /></span>
          </span>
          <strong>ENTER THE LAB</strong>
          <i className={styles.entryArrow} aria-hidden="true">↗</i>
        </a>
      </header>

      <div className={styles.universe} aria-label="Kent's Lab 技术实验轨道">
        <svg
          className={styles.orbits}
          viewBox="0 0 1000 760"
          role="img"
          aria-label="由区块链、稳定币、EVM 和 AI 关键词组成的实验轨道"
        >
          <defs>
            <path id="kent-orbit-outer" pathLength="1000" d="M500 52 C620 34 724 72 806 140 C902 184 944 282 922 378 C945 478 892 570 802 620 C712 690 610 694 500 670 C390 696 286 676 204 614 C110 568 64 478 82 378 C62 278 112 190 202 142 C286 70 390 35 500 52 Z" />
            <path id="kent-orbit-middle" pathLength="1000" d="M500 104 C602 90 690 118 758 172 C840 208 874 288 858 378 C875 462 830 526 758 574 C680 628 594 628 500 610 C406 630 318 610 248 562 C168 522 130 454 144 378 C128 292 170 222 246 178 C318 120 406 88 500 104 Z" />
            <path id="kent-orbit-inner" pathLength="1000" d="M500 164 C582 150 650 172 708 214 C772 246 802 304 790 378 C804 444 768 498 708 534 C648 576 574 574 500 558 C426 578 354 560 296 522 C234 490 202 434 214 378 C202 314 234 256 296 222 C354 174 424 150 500 164 Z" />
          </defs>

          <g className={styles.contours}>
            <use href="#kent-orbit-outer" />
            <use href="#kent-orbit-middle" />
            <use href="#kent-orbit-inner" />
            <path d="M500 222 C560 212 618 230 658 260 C708 284 730 326 720 378 C730 428 704 466 658 494 C612 526 556 522 500 512 C442 526 388 512 344 484 C296 458 274 422 282 378 C274 330 298 290 344 264 C388 232 444 210 500 222 Z" />
          </g>

          <g className={`${styles.orbitText} ${styles.orbitTextOuter}`}>
            <text>
              <textPath href="#kent-orbit-outer" startOffset="1%">
                KENT&apos;S LAB · BLOCKCHAIN · STABLECOIN · PRIVACY ·
                <animate attributeName="startOffset" values="1%;30%;1%" keyTimes="0;0.5;1" dur="80s" repeatCount="indefinite" />
              </textPath>
            </text>
          </g>
          <g className={`${styles.orbitText} ${styles.orbitTextMiddle}`}>
            <text>
              <textPath href="#kent-orbit-middle" startOffset="55%">
                智能合约 · 工程实践 · 技术研究 · 工作复盘 ·
                <animate attributeName="startOffset" values="55%;8%;55%" keyTimes="0;0.5;1" dur="68s" repeatCount="indefinite" />
              </textPath>
            </text>
          </g>
          <g className={`${styles.orbitText} ${styles.orbitTextInner}`}>
            <text>
              <textPath href="#kent-orbit-inner" startOffset="4%">
                EVM · SOLIDITY · GAS · ZK · MPC · RUST ·
                <animate attributeName="startOffset" values="4%;36%;4%" keyTimes="0;0.5;1" dur="48s" repeatCount="indefinite" />
              </textPath>
            </text>
          </g>
        </svg>

        <div className={styles.core} aria-label="Kent's Lab 实验核心">
          <div className={styles.coreGlow} aria-hidden="true" />
          <div className={styles.eyes} aria-hidden="true">
            <span className={styles.eye}><i /></span>
            <span className={styles.eye}><i /></span>
          </div>
          <div className={styles.coreLabel}>
            <span>KENT&apos;S</span>
            <strong>LAB</strong>
          </div>
          <span className={styles.coreMeta}>EST. 2026 · BEIJING</span>
        </div>

        <span className={`${styles.annotation} ${styles.annotationOne}`}>01 / EXPLORE</span>
        <span className={`${styles.annotation} ${styles.annotationTwo}`}>IDEAS → CODE</span>
        <span className={`${styles.annotation} ${styles.annotationThree}`}>BUILD · TEST · WRITE</span>
      </div>

      <p className={styles.scrollHint}><span /> SCROLL TO EXPLORE</p>
    </section>
  )
}
