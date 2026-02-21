const VARIANT_CLASS = {
  easy: 'badge-easy',
  moderate: 'badge-moderate',
  hard: 'badge-hard',
  improving: 'badge-improving',
  stable: 'badge-stable',
  regressing: 'badge-regressing',
};

export default function Badge({ label, variant = 'stable' }) {
  return (
    <span className={`badge ${VARIANT_CLASS[variant] || 'badge-stable'}`}>
      {label}
    </span>
  );
}
