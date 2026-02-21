export default function Button({ label, onClick, disabled = false, loading = false, variant = 'primary', type = 'button' }) {
  return (
    <button
      type={type}
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? <span className="btn-spinner" /> : label}
    </button>
  );
}
