# Platform Override: Print / Brand Collateral

Applies to: product datasheets, brochures, trade show materials, packaging, executive presentations (PowerPoint / Keynote), event signage, merchandise.

---

## Typography

| Context | Font | Weights |
|---------|------|---------|
| All headings, display text | Sequel100 | Wide 45 (body weight), Wide 65 (bold) |
| Body copy, captions | Roboto | 400, 500 |
| Data tables, specs | Roboto Mono | 400 |

- Sora is **not used** in print — Sequel100 is the print-exclusive headline face.
- Minimum body copy size: 8pt. Preferred: 10pt.
- Line height: 1.4–1.6× for body, 1.1–1.2× for display.
- Label / sublabel: Sora may appear in digital-first PDFs (screened at 72–96dpi) but Sequel100 is preferred for print output.

---

## Color — Print Profiles

| Profile | Use when |
|---------|----------|
| **CMYK (Coated)** | Offset printing, high-quality brochures |
| **CMYK (Uncoated)** | Matte paper, merchandise, packaging |
| **RGB** | Digital PDFs, presentation decks, screen-only exports |
| **Pantone** | Single-color or spot-color print jobs |

### Core Brand Colors (Print)

| Token | RGB | CMYK (approx.) | Pantone (approx.) |
|-------|-----|----------------|-------------------|
| Solidigm Purple | `#4F00B5` | C87 M100 Y0 K0 | 2735 C |
| Electric Teal | `#00FFEC` | C100 M0 Y7 K0 | 3255 C |
| Black | `#000000` | C0 M0 Y0 K100 | Black C |
| White | `#FFFFFF` | — | — |

> Always verify Pantone matches with print vendor. These are approximations.

---

## Layout & Spacing

- US Letter (8.5×11") and A4 are primary document sizes.
- Trade show banners: 33×81", 10×8 ft.
- Bleed: 0.125" / 3mm on all sides.
- Safe area: 0.25" / 6mm from trim.
- Grid: 12-column on letter/A4. Column gutter: 4mm (≈ `space.1`).
- **The 4px web grid does not apply to print.** Use mm/pt units.

---

## Notch / Shape

- The 45° notch appears in print as a clipped corner on hero images, section dividers, and full-bleed graphics.
- Cut sizes: `sm=96px` (screen equivalent) scales to ~25mm in A4, ~30mm in US Letter.
- See `tokens/shape.json` for all notch dimensions.

---

## Logo Usage

- Use `.eps` or `.pdf` for print. Never `.png` or `.svg` for offset printing unless confirmed with vendor.
- Minimum print size: 1" (25mm) wide.
- Clear space: equal to the height of the "S" in Solidigm on all sides.
- See `brand/logo.md` for full rules.

---

## Imagery

- Resolution: 300dpi minimum at final placement size.
- Product renders: use master files from SharePoint `Files/12 - Product Renders`.
- Photography: follow brand photography guidelines in `brand/photography.md`.

---

## Do Nots

- Do not use Sora as the primary typeface for print — use Sequel100.
- Do not reproduce Electric Teal as a process CMYK mix on uncoated stock — it will appear muddy. Use Pantone 3255 C.
- Do not scale the logo below 1" wide.
- Do not use web hex values without converting to appropriate print profile.
