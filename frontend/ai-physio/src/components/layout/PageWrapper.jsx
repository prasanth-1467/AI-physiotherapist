export default function PageWrapper({ children, title }) {
  return (
    <div className="page-wrapper">
      <div className="page-inner">
        {title && <h1 className="page-title">{title}</h1>}
        {children}
      </div>
    </div>
  );
}
