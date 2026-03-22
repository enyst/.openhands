# Broadsheet Dispatch

**Vibe:** Newspaper front page, authoritative, status-rich, editorial

**Layout:** Broadsheet grid with a metadata rail, ticker strip, lead story area, sidebars, and classified-style notices. Each slide should still fit exactly in the viewport; think “front page compressed into one screen,” not an infinitely scrolling article.

**Typography:**
- Display: `Cormorant Garamond` (700) or `Bodoni Moda` (700) for mastheads and banner headlines
- Body: `Source Serif 4` (400/600)
- Labels / metadata: `IBM Plex Sans Condensed` or `Arial Narrow`

**Colors:**
```css
:root {
    --bg-paper: #f6efe2;
    --ink: #191713;
    --text-muted: #6b6357;
    --rule: #1f1a15;
    --accent-crimson: #a32622;
    --accent-blue: #294663;
    --accent-green: #2d6b42;
}
```

**Signature Elements:**
- Oversized centered masthead with top metadata rail
- Black ticker strip for all-caps headlines
- Large all-caps lead headline with tight tracking
- Multi-column article grids, drop caps, pull quotes
- Boxed sidebars, status cards, and classified-style notices
- Narrow uppercase status badges in red / blue / green
- **No illustrations—use borders, rules, boxes, and typography as the visual system**

**Best For:**
- Status newsletters
- Technical weekly digests
- PR / issue roundups
- Release-room briefings

---
