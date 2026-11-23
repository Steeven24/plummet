// Small line icons. They look the same on every system, unlike emoji.

const base = {
  width: 16,
  height: 16,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export const BellIcon = () => (
  <svg {...base}>
    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
    <path d="M10.3 21a1.9 1.9 0 0 0 3.4 0" />
  </svg>
);

export const BellOffIcon = () => (
  <svg {...base}>
    <path d="M8.7 3A6 6 0 0 1 18 8c0 2.4.4 4.2 1 5.6M17 17H3s3-2 3-9c0-.8.2-1.6.5-2.3" />
    <path d="M10.3 21a1.9 1.9 0 0 0 3.4 0M2 2l20 20" />
  </svg>
);

export const TrashIcon = () => (
  <svg {...base}>
    <path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14" />
  </svg>
);

export const CheckIcon = () => (
  <svg {...base}>
    <path d="M5 12l5 5L20 7" />
  </svg>
);
