# Header Section

**Node ID**: 123:456  
**Figma URL**: [View in Figma](https://figma.com/file/ABC123?node-id=123:456)  
**Status**: ✅ Verified  
**Last Updated**: 2026-01-27

---

## 📐 Layout Specifications

| Property  | Value         |
| --------- | ------------- |
| Width     | 1440px        |
| Height    | 80px          |
| Padding   | 20px 40px     |
| Gap       | 24px          |
| Direction | Horizontal    |
| Alignment | Center        |
| Justify   | Space Between |

### CSS Equivalent

```css
.header {
  width: 100%;
  max-width: 1440px;
  height: 80px;
  padding: 20px 40px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
```

### Tailwind Classes

```html
<header
  class="w-full max-w-[1440px] h-20 px-10 py-5 flex flex-row items-center justify-between gap-6"
></header>
```

---

## 🧩 Components

### 1. Logo (Component Instance)

- **Type**: Component Instance
- **Component ID**: 456:789
- **Override Text**: "MyBrand"
- **Constraints**: Left-aligned, vertically centered

```tsx
<Logo text="MyBrand" />
```

### 2. Navigation

- **Type**: Frame (Auto-layout)
- **Gap**: 32px
- **Items**: 3 navigation links

**Nav Items:**

1. Products
2. Solutions
3. Pricing

**Text Style:**

- Font: Inter, 16px
- Line Height: 24px
- Weight: 500
- Color: #374151

**Hover State:**

- Color: #1F2937

```tsx
<nav className="flex gap-8">
  <a href="/products" className="text-gray-700 hover:text-gray-900">
    Products
  </a>
  <a href="/solutions" className="text-gray-700 hover:text-gray-900">
    Solutions
  </a>
  <a href="/pricing" className="text-gray-700 hover:text-gray-900">
    Pricing
  </a>
</nav>
```

### 3. CTA Button (Component Instance)

- **Type**: Button/Primary
- **Component ID**: 789:012
- **Override Text**: "Get Started"
- **Background**: #3B82F6
- **Text Color**: #FFFFFF
- **Action**: Navigate to /signup

```tsx
<Button variant="primary" onClick={() => navigate("/signup")}>
  Get Started
</Button>
```

---

## 🎨 Assets

### Search Icon

- **Format**: SVG Vector
- **Dimensions**: 24x24px
- **Color**: #6B7280
- **Path**: Magnifying glass icon

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
        stroke="#6B7280"
        stroke-width="2"
        stroke-linecap="round"/>
</svg>
```

---

## 🎭 Interactions

| Trigger | Target         | Action       | Value   |
| ------- | -------------- | ------------ | ------- |
| Hover   | Nav-Item       | Change Color | #1F2937 |
| Click   | Button/Primary | Navigate     | /signup |

---

## ♿ Accessibility

- [ ] Add `role="navigation"` to nav element
- [ ] Ensure button has proper focus states
- [ ] Add ARIA label to search icon
- [ ] Ensure color contrast meets WCAG AA (4.5:1)

---

## 📱 Responsive Behavior

**Desktop (1440px+)**

- Full layout as specified

**Tablet (768px - 1439px)**

- Reduce horizontal padding to 24px
- Maintain gap spacing

**Mobile (< 768px)**

- Stack navigation vertically or use hamburger menu
- Reduce padding to 16px
- Consider hiding search on mobile

---

## 💻 Implementation Code

### React + Tailwind

```tsx
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/common/Button";

export function Header() {
  return (
    <header className="w-full max-w-[1440px] h-20 px-10 py-5 flex items-center justify-between gap-6">
      {/* Logo */}
      <Logo text="MyBrand" />

      {/* Navigation */}
      <nav className="flex gap-8" role="navigation">
        <a
          href="/products"
          className="text-gray-700 hover:text-gray-900 font-medium transition-colors"
        >
          Products
        </a>
        <a
          href="/solutions"
          className="text-gray-700 hover:text-gray-900 font-medium transition-colors"
        >
          Solutions
        </a>
        <a
          href="/pricing"
          className="text-gray-700 hover:text-gray-900 font-medium transition-colors"
        >
          Pricing
        </a>
      </nav>

      {/* CTA Button */}
      <Button
        variant="primary"
        onClick={() => (window.location.href = "/signup")}
      >
        Get Started
      </Button>
    </header>
  );
}
```

### TypeScript Types

```typescript
interface HeaderProps {
  className?: string;
}

interface NavItem {
  label: string;
  href: string;
}

const navItems: NavItem[] = [
  { label: "Products", href: "/products" },
  { label: "Solutions", href: "/solutions" },
  { label: "Pricing", href: "/pricing" },
];
```

---

## 📝 Implementation Notes

1. **Logo Component**: Reusable component from `/components/common/Logo`
2. **Button Component**: Use primary variant from design system
3. **Navigation**: Consider extracting to separate component if used elsewhere
4. **Responsive**: Implement mobile menu for screens < 768px
5. **Performance**: Logo should be optimized SVG or WebP
6. **SEO**: Use semantic HTML5 `<header>` and `<nav>` tags

---

## ✅ Verification Checklist

- [x] Layout matches Figma dimensions
- [x] All text content extracted (not defaults)
- [x] Component overrides captured
- [x] Colors verified against design
- [x] Interactions documented
- [x] Assets downloaded
- [x] Accessibility considerations noted
- [x] Code examples provided
