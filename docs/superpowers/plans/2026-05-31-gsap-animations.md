# GSAP 全站动效 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add GSAP-powered scroll and hover animations to the Hugo beauty blog for a polished interactive experience.

**Architecture:** Load GSAP + ScrollTrigger from CDN at page footer, then run all animation logic from a single partial. Use `gsap.matchMedia()` for accessibility (respect `prefers-reduced-motion`) and responsive breakpoints. Use `ScrollTrigger.batch()` for efficient card/paragraph entrances.

**Tech Stack:** GSAP 3 + ScrollTrigger (CDN), Hugo templates, vanilla JS

---

### Task 1: Modify footer.html — load GSAP scripts and animations partial

**Files:**
- Modify: `layouts/partials/footer.html:59` (before `{{- partial "extend_footer.html" . }}`)

- [ ] **Step 1: Add GSAP CDN scripts and animations partial**

In `layouts/partials/footer.html`, find this line:
```
{{- partial "extend_footer.html" . }}
```

Replace it with:

```html
{{- if not (site.Params.disableGSAP | default false) }}
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
{{- end }}
{{- partial "gsap-animations.html" . }}
```

- [ ] **Step 2: Commit**

```bash
git add layouts/partials/footer.html
git commit -m "feat: add GSAP script loading in footer"
```

---

### Task 2: Create gsap-animations.html — all animation logic

**Files:**
- Create: `layouts/partials/gsap-animations.html`

This file contains ALL GSAP animation code. It runs at page load and uses `gsap.matchMedia()` for accessibility.

- [ ] **Step 1: Create the animations partial**

Create `layouts/partials/gsap-animations.html` with the following complete content:

```html
{{- if not (site.Params.disableGSAP | default false) }}
<script>
if (typeof gsap !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);

  let mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const isList = document.body.classList.contains("list");
    const isSingle = !isList && document.querySelector(".post-single");
    const isMobile = window.innerWidth < 768;

    // ===== A. Navigation auto-hide (desktop only) =====
    if (!isMobile) {
      let lastScroll = 0;
      const header = document.querySelector(".header");
      if (header) {
        ScrollTrigger.create({
          onUpdate: (self) => {
            const scrollY = window.scrollY;
            if (scrollY > 50 && self.direction === 1) {
              gsap.to(header, { y: "-100%", duration: 0.3, ease: "power2.out", overwrite: "auto" });
            } else if (self.direction === -1) {
              gsap.to(header, { y: "0%", duration: 0.3, ease: "power2.out", overwrite: "auto" });
            }
            lastScroll = scrollY;
          }
        });
      }
    }

    // ===== B. Menu hover effect =====
    document.querySelectorAll("#menu a").forEach(link => {
      link.addEventListener("mouseenter", function() {
        gsap.to(this, { color: "var(--secondary)", duration: 0.2, ease: "power2.out" });
      });
      link.addEventListener("mouseleave", function() {
        gsap.to(this, { color: "var(--primary)", duration: 0.3, ease: "power2.out" });
      });
    });

    // ===== C. Card grid scroll entrance (list pages) =====
    if (isList) {
      ScrollTrigger.batch(".post-card", {
        start: "top 90%",
        once: true,
        onEnter: (batch) => {
          gsap.fromTo(batch,
            { y: 60, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.6, ease: "power2.out", stagger: isMobile ? 0.05 : 0.1, overwrite: true }
          );
        }
      });
    }

    // ===== D. Card hover enhancement (list pages) =====
    if (isList) {
      document.querySelectorAll(".post-card").forEach(card => {
        card.addEventListener("mouseenter", function() {
          gsap.to(this, { y: -6, boxShadow: "0 12px 32px rgba(0,0,0,0.15)", duration: 0.3, ease: "power2.out", overwrite: "auto" });
        });
        card.addEventListener("mouseleave", function() {
          gsap.to(this, { y: 0, boxShadow: "none", duration: 0.3, ease: "power2.out", overwrite: "auto" });
        });
      });
    }

    // ===== E. Article title elastic entrance (single page) =====
    if (isSingle) {
      const title = document.querySelector(".post-single .post-title");
      if (title) {
        gsap.from(title, { y: -30, opacity: 0, scale: 0.95, duration: 0.8, ease: "back.out(1.7)", delay: 0.1 });
      }
    }

    // ===== F. Featured image fade-in (single page) =====
    if (isSingle) {
      const coverImg = document.querySelector(".post-single .entry-cover img");
      if (coverImg) {
        gsap.fromTo(coverImg, { scale: 1.08, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8, ease: "power2.out", delay: 0.2 });
      }
    }

    // ===== G. Content paragraphs scroll entrance (single page) =====
    if (isSingle) {
      const contentEl = document.querySelector(".post-single .post-content");
      if (contentEl) {
        const elements = contentEl.querySelectorAll("p, h2, h3, h4, .post-content > ul, .post-content > ol, .post-content > blockquote");
        if (elements.length) {
          ScrollTrigger.batch(elements, {
            start: "top 85%",
            once: true,
            onEnter: (batch) => {
              gsap.fromTo(batch,
                { y: 24, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, ease: "power1.out", stagger: isMobile ? 0.03 : 0.06, overwrite: true }
              );
            }
          });
        }
      }
    }

    // ===== H. Article images scroll reveal (single page) =====
    if (isSingle) {
      const contentImgs = document.querySelectorAll(".post-single .post-content img");
      if (contentImgs.length) {
        ScrollTrigger.batch(contentImgs, {
          start: "top 85%",
          once: true,
          onEnter: (batch) => {
            gsap.fromTo(batch,
              { scale: 0.95, opacity: 0 },
              { scale: 1, opacity: 1, duration: 0.7, ease: "power2.out", overwrite: true }
            );
          }
        });
      }
    }

    // ===== I. Tags staggered entrance (single page) =====
    if (isSingle) {
      const tagItems = document.querySelectorAll(".post-tags li");
      if (tagItems.length) {
        ScrollTrigger.batch(tagItems, {
          start: "top 95%",
          once: true,
          onEnter: (batch) => {
            gsap.fromTo(batch,
              { y: 16, opacity: 0 },
              { y: 0, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.05, overwrite: true }
            );
          }
        });
      }
    }

    // ===== J. Footer fade-in =====
    const footer = document.querySelector(".footer");
    if (footer) {
      ScrollTrigger.create({
        trigger: footer,
        start: "top 95%",
        once: true,
        onEnter: () => {
          gsap.fromTo(footer, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" });
        }
      });
    }

    // ===== K. Back to top button GSAP enhancement =====
    // Note: replaces the existing window.onscroll in footer.html
    const topLink = document.getElementById("top-link");
    if (topLink) {
      let isVisible = false;
      window.onscroll = function() {
        const scrollThreshold = window.innerHeight;
        const shouldShow = document.body.scrollTop > scrollThreshold || document.documentElement.scrollTop > scrollThreshold;
        if (shouldShow && !isVisible) {
          isVisible = true;
          topLink.classList.remove("hidden");
          gsap.fromTo(topLink, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)", overwrite: true });
        } else if (!shouldShow && isVisible) {
          isVisible = false;
          gsap.to(topLink, { scale: 0, opacity: 0, duration: 0.2, ease: "power2.in", overwrite: true, onComplete: () => {
            topLink.classList.add("hidden");
            gsap.set(topLink, { clearProps: "all" });
          }});
        }
      };

      topLink.addEventListener("click", function(e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
        if (window.history.pushState) {
          history.replaceState(null, null, " ");
        }
      });
    }

    return () => {
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  });
}
</script>
{{- end }}
```

- [ ] **Step 2: Commit**

```bash
git add layouts/partials/gsap-animations.html
git commit -m "feat: add GSAP animations partial with all site animations"
```

---

### Task 3: Update custom.css — theme transition

**Files:**
- Modify: `assets/css/extended/custom.css`

- [ ] **Step 1: Add theme transition CSS**

Add at the end of `assets/css/extended/custom.css`:

```css
/* Theme transition */
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/extended/custom.css
git commit -m "feat: add smooth theme transition"
```

---

### Task 4: Build and verify

- [ ] **Step 1: Initialize theme submodule if needed**

```bash
git submodule update --init --recursive
```

- [ ] **Step 2: Install npm dependencies**

```bash
npm install
```

- [ ] **Step 3: Build the site with Hugo**

```bash
hugo --minify
```

Expected: Site builds without errors. Check `public/` directory exists.

- [ ] **Step 4: Verify GSAP scripts are in built output**

```bash
grep -c "gsap" public/**/*.html | head -20
```

Expected: Multiple matches (gsap CDN URLs and animation code in the output).

- [ ] **Step 5: Commit the final state**

```bash
git add -A
git commit -m "feat: complete GSAP animation system"
```
