export default function Card({ header, children, footer, variant = 'default', className = '' }) {
  return (
    <div className={`card card-${variant} ${className}`}>
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}
