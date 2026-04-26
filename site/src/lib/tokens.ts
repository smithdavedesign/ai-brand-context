/**
 * Token loaders — pulls values directly from the source tokens JSON in the repo root.
 * This is how the site dogfoods @solidigm/brand-tokens.
 */
import colorsJson from '../../../tokens/colors.json';
import typographyJson from '../../../tokens/typography.json';
import motionJson from '../../../tokens/motion.json';
import elevationJson from '../../../tokens/elevation.json';
import breakpointsJson from '../../../tokens/breakpoints.json';

export interface ColorToken {
  name: string;
  hex: string;
  cssVar: string;
  group: 'Dark' | 'Light' | 'Accents';
  tokenPath: string;
}

export interface TypeToken {
  name: string;
  scale: 'Desktop' | 'Mobile';
  fontFamily: string;
  fontSize: string;
  fontWeight: number;
  lineHeight: string;
  letterSpacing: string;
  textTransform: string;
}

const cssVarMap: Record<string, string> = {
  'Solidigm Purple': '--color-purple-500',
  'Light Purple': '--color-purple-400',
  'Dark Purple': '--color-purple-600',
  'Ultra Dark Purple': '--color-purple-900',
  'Dark Blue': '--color-blue-900',
  'Dark Grey': '--color-neutral-800',
  Black: '--color-neutral-900',
  White: '--color-neutral-0',
  'Light Gray': '--color-neutral-50',
  Gray: '--color-neutral-300',
  'Medium Gray': '--color-neutral-600',
  'Electric Teal': '--color-accent-teal',
  'Electric Pink': '--color-accent-pink',
  Orange: '--color-accent-orange',
};

export function getColorTokens(): ColorToken[] {
  const out: ColorToken[] = [];
  for (const [group, entries] of Object.entries(colorsJson as Record<string, Record<string, { $value: string }>>)) {
    for (const [name, meta] of Object.entries(entries)) {
      out.push({
        name,
        hex: meta.$value,
        cssVar: cssVarMap[name] ?? `--color-${name.toLowerCase().replace(/\s+/g, '-')}`,
        group: group as ColorToken['group'],
        tokenPath: `${group}.${name}`,
      });
    }
  }
  return out;
}

export function getTypeTokens(): TypeToken[] {
  const out: TypeToken[] = [];
  for (const [scale, entries] of Object.entries(typographyJson as Record<string, Record<string, { $value: TypeToken }>>)) {
    for (const [name, meta] of Object.entries(entries)) {
      out.push({
        name,
        scale: scale as TypeToken['scale'],
        ...meta.$value,
      });
    }
  }
  return out;
}

/** Spacing scale — sourced from ui-toolkit.min.css --space-N variables. */
export const spacingScale: { token: string; value: string }[] = [
  { token: '--space-0', value: '0px' },
  { token: '--space-1', value: '4px' },
  { token: '--space-2', value: '8px' },
  { token: '--space-3', value: '12px' },
  { token: '--space-4', value: '16px' },
  { token: '--space-5', value: '20px' },
  { token: '--space-6', value: '24px' },
  { token: '--space-7', value: '28px' },
  { token: '--space-8', value: '32px' },
  { token: '--space-9', value: '40px' },
  { token: '--space-10', value: '48px' },
  { token: '--space-11', value: '56px' },
  { token: '--space-12', value: '64px' },
  { token: '--space-13', value: '72px' },
  { token: '--space-14', value: '80px' },
  { token: '--space-15', value: '88px' },
  { token: '--space-16', value: '96px' },
];

export const radiusScale = [
  { token: '--border-radius-sm', value: '8px', use: 'Buttons, inputs, small chips' },
  { token: '--border-radius-md', value: '16px', use: 'Cards, containers, modals' },
  { token: '--border-radius-lg', value: '16px', use: 'Large surfaces (same as md today)' },
];

export const semanticColors = [
  { name: 'Error', hex: '#ba3640', cssVar: '--color-semantic-error', use: 'Destructive actions, error text, validation' },
  { name: 'Warning', hex: '#ff0000', cssVar: '--color-semantic-warning', use: 'Critical alerts (use sparingly)' },
];

/** WCAG 2.1 relative luminance contrast ratio. */
export function contrastRatio(hexA: string, hexB: string): number {
  const L = (hex: string) => {
    const h = hex.replace('#', '');
    const r = parseInt(h.substring(0, 2), 16) / 255;
    const g = parseInt(h.substring(2, 4), 16) / 255;
    const b = parseInt(h.substring(4, 6), 16) / 255;
    const toLin = (c: number) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
    return 0.2126 * toLin(r) + 0.7152 * toLin(g) + 0.0722 * toLin(b);
  };
  const l1 = L(hexA);
  const l2 = L(hexB);
  const [a, b] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (a + 0.05) / (b + 0.05);
}

// ---------------------------------------------------------------------------
// Motion tokens
// ---------------------------------------------------------------------------

export interface MotionDuration {
  name: string;
  value: string;
  description: string;
}

export interface MotionEasing {
  name: string;
  cssValue: string;
  rawValue: number[];
  description: string;
}

type MotionJson = typeof motionJson;

export function getMotionDurations(): MotionDuration[] {
  const durations = (motionJson as MotionJson).duration as Record<string, { $value: string; $description: string }>;
  return Object.entries(durations).map(([name, tok]) => ({
    name,
    value: tok.$value,
    description: tok.$description,
  }));
}

export function getMotionEasings(): MotionEasing[] {
  const easings = (motionJson as MotionJson).easing as Record<string, { $value: number[]; $description: string }>;
  return Object.entries(easings).map(([name, tok]) => ({
    name,
    rawValue: tok.$value,
    cssValue: `cubic-bezier(${tok.$value.join(', ')})`,
    description: tok.$description,
  }));
}

// ---------------------------------------------------------------------------
// Elevation tokens
// ---------------------------------------------------------------------------

export interface ShadowToken {
  name: string;
  cssValue: string;
  description: string;
}

type ElevationJson = typeof elevationJson;

export function getShadowTokens(): ShadowToken[] {
  const shadows = (elevationJson as ElevationJson).shadow as Record<string, { $value: string | Record<string, string | number | boolean>; $description: string }>;
  return Object.entries(shadows).map(([name, tok]) => {
    let cssValue: string;
    if (typeof tok.$value === 'string') {
      cssValue = tok.$value;
    } else {
      const s = tok.$value as Record<string, string | number | boolean>;
      const inset = s.inset ? 'inset ' : '';
      cssValue = `${inset}${s.offsetX} ${s.offsetY} ${s.blur} ${s.spread} ${s.color}`;
    }
    return { name, cssValue, description: tok.$description };
  });
}

// ---------------------------------------------------------------------------
// Breakpoints tokens
// ---------------------------------------------------------------------------

export interface BreakpointToken {
  name: string;
  value: string;
  description: string;
}

type BreakpointsJson = typeof breakpointsJson;

export function getBreakpointTokens(): BreakpointToken[] {
  const bps = (breakpointsJson as BreakpointsJson).breakpoint as Record<string, { $value: string; $description: string }>;
  return Object.entries(bps).map(([name, tok]) => ({
    name,
    value: tok.$value,
    description: tok.$description,
  }));
}

export function getContainerTokens(): BreakpointToken[] {
  const containers = (breakpointsJson as BreakpointsJson).container as Record<string, { $value: string; $description: string }>;
  return Object.entries(containers).map(([name, tok]) => ({
    name,
    value: tok.$value,
    description: tok.$description,
  }));
}
